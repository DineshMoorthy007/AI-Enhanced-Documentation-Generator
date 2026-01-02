from fastapi import APIRouter, HTTPException
import requests

from models.schemas import RepoRequest

router = APIRouter()

@router.post("/validate-repo")
def validate_repo(data: RepoRequest):
    repo_url = str(data.repo_url)

    # Convert GitHub URL to API URL
    # https://github.com/user/repo -> https://api.github.com/repos/user/repo
    if "github.com" not in repo_url:
        raise HTTPException(status_code=400, detail="Not a GitHub URL")

    api_url = repo_url.replace("https://github.com/", "https://api.github.com/repos/")

    response = requests.get(api_url)

    if response.status_code != 200:
        raise HTTPException(status_code=404, detail="Repository not found or inaccessible")

    return {
        "status": "valid",
        "repo": repo_url
    }

from services.github_service import get_repo_file_tree ,filter_source_files


@router.post("/debug/filtered-files")
def debug_filtered_files(data: RepoRequest):
    repo_url = str(data.repo_url)

    parts = repo_url.replace("https://github.com/", "").split("/")
    owner, repo = parts[0], parts[1]

    files = get_repo_file_tree(owner, repo)
    filtered = filter_source_files(files)

    return {
        "total_files": len(files),
        "filtered_files": len(filtered),
        "sample": filtered[:20]
    }

from services.parser_service import extract_functions_and_classes

@router.post("/debug/parse-code")
def debug_parse_code():
    sample_code = """
    function loginUser(email, password) {
        return true;
    }

    const fetchData = () => {
        return [];
    }

    class AuthService {
        constructor() {}
    }
    """

    return extract_functions_and_classes(sample_code)

from services.github_service import fetch_file_content ,get_default_branch

@router.post("/debug/parse-real-files")
def debug_parse_real_files(data: RepoRequest):
    repo_url = str(data.repo_url)

    parts = repo_url.replace("https://github.com/", "").split("/")
    owner, repo = parts[0], parts[1]

    branch = get_default_branch(owner, repo)
    all_files = get_repo_file_tree(owner, repo)
    source_files = filter_source_files(all_files)

    results = []

    # Limit to first 3 files for safety
    for file_path in source_files[:3]:
        code = fetch_file_content(owner, repo, branch, file_path)
        parsed = extract_functions_and_classes(code)

        results.append({
            "file": file_path,
            "functions": parsed["functions"],
            "classes": parsed["classes"],
        })

    return {
        "parsed_files": results
    }

