from typing import Optional, List
from pydantic import BaseModel, HttpUrl


class QueryPayload(BaseModel):
    query: str


class processPDFPayload(BaseModel):
    fileUrl: HttpUrl
