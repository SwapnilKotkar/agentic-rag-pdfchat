import pytesseract
from pdf2image import convert_from_path
from typing import Generator
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings, GoogleGenerativeAI
from server.config import connectToOpensearch
import hashlib
from datetime import datetime
import os
from langchain.prompts import PromptTemplate
from langchain.chains.llm import LLMChain

# from langchain.vectorstores import OpenSearchVectorSearch
from langchain_community.vectorstores import OpenSearchVectorSearch
from langchain.chains.retrieval_qa.base import RetrievalQA

pytesseract.pytesseract.tesseract_cmd = (
    r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
)

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500, chunk_overlap=50, separators=["\n\n", "\n", ".", " ", ""]
)

llm = GoogleGenerativeAI(model="gemini-1.5-flash-latest")
embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")


def ocr_pdf_pages(pdf_path: str) -> Generator[tuple[int, str], None, None]:
    images = convert_from_path(
        pdf_path, poppler_path=r"C:\\poppler\\poppler-24.08.0\\Library\\bin"
    )
    for i, img in enumerate(images):
        text = pytesseract.image_to_string(img)
        yield i + 1, text


def generate_chunk_id(chunk: str, source: str, page: int) -> str:
    key = f"{source}-{page}-{chunk}"
    return hashlib.sha256(key.encode("utf-8")).hexdigest()


def split_and_store_vectors(pdf_path: str):
    print("Processing PDF:", pdf_path)
    filename = os.path.basename(pdf_path)
    processed_at = datetime.utcnow().isoformat()

    result = connectToOpensearch()
    if result is None:
        print("OpenSearch connection failed. Cannot proceed.")
        return

    client, index_name = result
    print("Connected to OpenSearch.")

    for page_num, text in ocr_pdf_pages(pdf_path):
        chunks = splitter.split_text(text)
        print(f"Page {page_num}: {len(chunks)} chunks")

        for i, chunk in enumerate(chunks):
            try:
                chunk_id = generate_chunk_id(chunk, filename, page_num)

                exists = client.exists(index=index_name, id=chunk_id)
                if exists:
                    print(f"Chunk {chunk_id} already exists, skipping...")
                    continue

                embedding_result = embeddings.embed_query(chunk)

                doc = {
                    "content": chunk,
                    "embedding": embedding_result,
                    "page": page_num,
                    "source": filename,
                    "processed_at": processed_at,
                }

                client.index(index=index_name, id=chunk_id, body=doc)
                print(f"Stored chunk {i + 1}/{len(chunks)} | ID: {chunk_id}")

            except Exception as e:
                print(f"Error storing chunk {i + 1} on page {page_num}: {e}")


def search_by_query(query: str) -> dict:
    top_k = 10

    result = connectToOpensearch()
    if result is None:
        return {"error": "Failed to connect to OpenSearch."}

    client, index_name = result

    try:
        # Setup OpenSearchVectorSearch retriever
        vectorstore = OpenSearchVectorSearch(
            opensearch_url="https://localhost:9200",  # Update with your URL
            http_auth=("admin", "Swapnil@1234#"),  # If authentication needed
            index_name=index_name,
            embedding_function=embeddings,
            use_ssl=True,
            verify_certs=False,
            ssl_show_warn=False,
        )

        retriever = vectorstore.as_retriever(search_kwargs={"k": top_k})

        # Setup LangChain QA Chain
        qa_chain = RetrievalQA.from_llm(
            llm=llm,
            retriever=retriever,
            return_source_documents=True,
            verbose=True,
        )

        # Perform semantic similarity search + answer generation
        response = qa_chain({"query": query})

        result_text = response.get("result", "")
        sources = [
            {
                "source": doc.metadata.get("source"),
                "page": doc.metadata.get("page"),
                "content": doc.page_content,
            }
            for doc in response.get("source_documents", [])
        ]

        return {
            "status": "success",
            "query": query,
            "answer": result_text,
            "retrieved_chunks": sources,
        }

    except Exception as e:
        return {"error": f"Search failed: {e}"}
