from fastapi import APIRouter, HTTPException
from fastapi.responses import Response

from models.schemas import RepoRequest
from services.doc_service import generate_readme_for_repo
import requests

router = APIRouter()


@router.post("/validate-repo")
def validate_repo(data: RepoRequest):
    repo_url = str(data.repo_url)

    if "github.com" not in repo_url:
        raise HTTPException(status_code=400, detail="Not a GitHub URL")

    api_url = repo_url.replace("https://github.com/", "https://api.github.com/repos/")
    response = requests.get(api_url)

    if response.status_code != 200:
        raise HTTPException(
            status_code=404,
            detail="Repository not found or inaccessible"
        )

    return {
        "status": "valid",
        "repo": repo_url
    }


@router.post("/generate-readme")
def generate_readme(data: RepoRequest):
    repo_url = str(data.repo_url)
    parts = repo_url.replace("https://github.com/", "").split("/")
    owner, repo = parts[0], parts[1]

    readme = generate_readme_for_repo(owner, repo, limit=5)

    return {
        "readme": readme
    }


@router.post("/download-readme")
def download_readme(data: RepoRequest):
    repo_url = str(data.repo_url)
    parts = repo_url.replace("https://github.com/", "").split("/")
    owner, repo = parts[0], parts[1]

    readme = generate_readme_for_repo(owner, repo, limit=5)

    return Response(
        content=readme,
        media_type="text/markdown",
        headers={
            "Content-Disposition": "attachment; filename=README.md"
        }
    )