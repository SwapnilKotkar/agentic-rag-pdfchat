from fastapi import APIRouter, HTTPException, Depends
from server.models.chat import QueryPayload, processPDFPayload
from server.services.process_pdf import split_and_store_vectors, search_by_query
import aiohttp
import tempfile
import os

# from bson import ObjectId
# from typing import List
# from motor.motor_asyncio import AsyncIOMotorDatabase

# from server.database import get_database
# from server.services.langchain import process_urls, searchByQuery

router = APIRouter()


@router.post("/process_pdf")
async def process_pdf(payload: processPDFPayload):
    file_url = payload.fileUrl

    print("file_url-----", file_url)

    try:
        # Download PDF to temp file
        async with aiohttp.ClientSession() as session:
            async with session.get(str(file_url)) as resp:
                if resp.status != 200:
                    raise HTTPException(status_code=400, detail="Download failed")

                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                    tmp.write(await resp.read())
                    pdf_path = tmp.name

        # Process PDF: split + generate + store vectors (only once per chunk)
        print("pdf_path_45454544", pdf_path)
        split_and_store_vectors(pdf_path)

        return {
            "message": "PDF processed and vectors stored.",
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {e}")

    finally:
        if os.path.exists(pdf_path):
            os.remove(pdf_path)


@router.post("/query")
async def query(payload: QueryPayload):
    query = payload.query
    print("query-----", query)
    result = search_by_query(query)
    print("result-----", result)
    return {
        "message": "Query received.",
        "result": result,
    }
