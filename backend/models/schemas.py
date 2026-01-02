from pydantic import BaseModel, HttpUrl

class RepoRequest(BaseModel):
    repo_url: HttpUrl
