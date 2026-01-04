from fastapi import APIRouter, HTTPException
from fastapi.responses import Response
from fastapi import UploadFile, File, Form
from typing import Optional

from models.schemas import RepoRequest
from services.doc_service import generate_readme_for_repo
import requests

from models.schemas import FileDocRequest
from services.parser_service import extract_functions_and_classes
from services.ai_service import generate_file_documentation
from services.readme_service import build_single_file_readme

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

@router.post("/generate-file-doc")
def generate_file_doc(data: FileDocRequest):
    filename = data.filename
    code = data.code

    if not code.strip():
        raise HTTPException(status_code=400, detail="Code content is empty")

    # Reuse your existing parser
    parsed = extract_functions_and_classes(code)

    # Reuse your existing AI logic
    documentation = generate_file_documentation(
        file_path=filename,
        functions=parsed["functions"],
        classes=parsed["classes"],
        code_snippet=code[:1500],  # safety limit
    )

    return {
        "file": filename,
        "functions": parsed["functions"],
        "classes": parsed["classes"],
        "documentation": documentation,
    }

@router.post("/generate-file-doc/upload")
async def generate_file_doc_upload(
    file: UploadFile = File(...),
    language: Optional[str] = Form(None),):

    filename = file.filename

    # Basic validation
    if not filename:
        raise HTTPException(status_code=400, detail="No file uploaded")

    # Read file content
    code_bytes = await file.read()
    code = code_bytes.decode("utf-8", errors="ignore")

    if not code.strip():
        raise HTTPException(status_code=400, detail="Uploaded file is empty")

    # Reuse existing parser
    parsed = extract_functions_and_classes(code)

    # Reuse AI documentation generator
    documentation = generate_file_documentation(
        file_path=filename,
        functions=parsed["functions"],
        classes=parsed["classes"],
        code_snippet=code[:1500],  # safety limit
    )

    return {
        "file": filename,
        "functions": parsed["functions"],
        "classes": parsed["classes"],
        "documentation": documentation,
    }

@router.post("/download-single-file-readme")
def download_single_file_readme(data: FileDocRequest):
    parsed = extract_functions_and_classes(data.code)

    documentation = generate_file_documentation(
        file_path=data.filename,
        functions=parsed["functions"],
        classes=parsed["classes"],
        code_snippet=data.code[:1500],
    )

    readme = build_single_file_readme(
        filename=data.filename,
        documentation=documentation,
        functions=parsed["functions"],
        classes=parsed["classes"],
    )

    return Response(
        content=readme,
        media_type="text/markdown",
        headers={
            "Content-Disposition": "attachment; filename=README.md"
        },
    )
