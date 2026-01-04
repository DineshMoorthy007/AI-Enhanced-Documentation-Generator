from pydantic import BaseModel, HttpUrl
from typing import Optional

class RepoRequest(BaseModel):
    repo_url: HttpUrl

class FileDocRequest(BaseModel):
    filename: str
    language: Optional[str] = None
    code: str
