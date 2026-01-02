import requests
import json
import os

GITHUB_API_BASE = "https://api.github.com"

def get_default_branch(owner: str, repo: str) -> str:
    repo_url = f"{GITHUB_API_BASE}/repos/{owner}/{repo}"
    response = requests.get(repo_url)

    if response.status_code != 200:
        raise Exception("Failed to fetch repository info")

    return response.json()["default_branch"]


def get_repo_file_tree(owner: str, repo: str):
    """
    Fetch the full recursive file tree of a GitHub repository.
    Returns a list of file paths.
    """
    # Step 1: Get default branch (usually main or master)
    repo_url = f"{GITHUB_API_BASE}/repos/{owner}/{repo}"
    repo_response = requests.get(repo_url)

    if repo_response.status_code != 200:
        raise Exception("Failed to fetch repository info")

    default_branch = repo_response.json()["default_branch"]

    # Step 2: Get the full tree recursively
    tree_url = f"{GITHUB_API_BASE}/repos/{owner}/{repo}/git/trees/{default_branch}?recursive=1"
    tree_response = requests.get(tree_url)

    if tree_response.status_code != 200:
        raise Exception("Failed to fetch repository file tree")

    tree_data = tree_response.json()["tree"]

    # Step 3: Extract only file paths
    file_paths = [
        item["path"]
        for item in tree_data
        if item["type"] == "blob"  # blob = file
    ]

    return file_paths

def load_ignored_folders():
    config_path = os.path.join(
        os.path.dirname(__file__),
        "..",
        "config",
        "file_filter.json"
    )

    with open(config_path, "r") as f:
        config = json.load(f)

    return config.get("ignored_folders", [])

def filter_source_files(file_paths):
    ignored_folders = load_ignored_folders()
    valid_extensions = (".js", ".ts")

    ignored_keywords = [
        "eslint",
        "prettier",
        "babel",
        "webpack",
        "config",
        "jest",
        "rollup"
    ]

    test_keywords = ["__tests__", "test", "spec", "e2e", "__mocks__"]

    filtered_files = []

    for path in file_paths:
        filename = os.path.basename(path).lower()
        path_lower = path.lower()

        # Rule 0: skip test files
        if any(keyword in path_lower for keyword in test_keywords):
            continue

        # Rule 1: extension check
        if not path_lower.endswith(valid_extensions):
            continue

        # Rule 2: ignore folders
        if any(folder in path_lower for folder in ignored_folders):
            continue

        # Rule 3: skip dotfiles
        if filename.startswith("."):
            continue

        # Rule 4: skip known config/tooling files
        if any(keyword in filename for keyword in ignored_keywords):
            continue

        filtered_files.append(path)

    return filtered_files

def fetch_file_content(owner: str, repo: str, branch: str, file_path: str):
    """
    Fetch raw file content from GitHub.
    """
    raw_url = (
        f"https://raw.githubusercontent.com/"
        f"{owner}/{repo}/{branch}/{file_path}"
    )

    response = requests.get(raw_url)

    if response.status_code != 200:
        raise Exception(f"Failed to fetch file: {file_path}")

    return response.text
