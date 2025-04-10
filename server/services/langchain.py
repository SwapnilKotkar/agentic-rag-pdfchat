# import os
# from typing import List

# from langchain.chains.retrieval_qa.base import RetrievalQA
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain_community.document_loaders import WebBaseLoader
# from langchain_community.vectorstores import FAISS
# from langchain_community.llms.openai import OpenAI
# from langchain_google_genai import GoogleGenerativeAIEmbeddings, GoogleGenerativeAI

# from dotenv import load_dotenv

# load_dotenv()

# huggingface_api_key = os.getenv("HUGGINGFACEHUB_API_TOKEN")
# groq_api_key = os.environ["GROQ_API_KEY"]
# google_api_key = os.environ["GOOGLE_API_KEY"]


# llm = GoogleGenerativeAI(model="gemini-1.5-flash-latest")
# embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")


# def process_urls(urls: List[str]) -> None:
#     """Process the URLs and store the data in a file."""

#     loader = WebBaseLoader(urls)
#     print("Data Loading...Started...✅✅✅")
#     data = loader.load()

#     text_splitter = RecursiveCharacterTextSplitter(
#         separators=["\n\n", "\n", ".", ",", " "],
#         chunk_size=1000,
#     )
#     print("Text Splitter...Started...✅✅✅")

#     docs = text_splitter.split_documents(data)

#     vectorstore = FAISS.from_documents(docs, embeddings)
#     print("Embedding Vector Started Building...✅✅✅")

#     vectorstore.save_local("faiss_index")


# def searchByQuery(query: str) -> dict:
#     """Search the query in the stored data."""

#     vectorstore = FAISS.load_local(
#         "faiss_index", embeddings, allow_dangerous_deserialization=True
#     )

#     chain = RetrievalQA.from_llm(
#         llm=llm,
#         retriever=vectorstore.as_retriever(search_kwargs={"k": 20}),
#         return_source_documents=True,
#         verbose=True,
#     )
#     response = chain({"query": query})

#     result_text = response.get("result", "")
#     sources = list(
#         set(
#             doc.metadata["source"]
#             for doc in response.get("source_documents", [])
#             if "source" in doc.metadata
#         )
#     )

#     return {"result": result_text, "sources": sources}
