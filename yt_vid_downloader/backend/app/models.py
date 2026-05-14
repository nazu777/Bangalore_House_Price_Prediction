from pydantic import BaseModel
from typing import List


class URLRequest(BaseModel):
    urls: List[str]


class DownloadRequest(BaseModel):
    urls: List[str]
    quality: str