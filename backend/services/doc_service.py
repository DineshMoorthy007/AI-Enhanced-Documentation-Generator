from services.github_service import (
    get_repo_file_tree,
    filter_source_files,
    fetch_file_content,
    get_default_branch,
)
from services.parser_service import extract_functions_and_classes
from services.ai_service import generate_file_documentation

_DOC_CACHE = {}

def generate_docs_for_repo(owner: str, repo: str, limit: int = 10):
    branch = get_default_branch(owner, repo)
    all_files = get_repo_file_tree(owner, repo)
    source_files = filter_source_files(all_files)

    docs = []

    for file_path in source_files[:limit]:
        code = fetch_file_content(owner, repo, branch, file_path)
        parsed = extract_functions_and_classes(code)

        cache_key = f"{repo}:{file_path}"

        # 1️. Use cache if available
        if cache_key in _DOC_CACHE:
            explanation = _DOC_CACHE[cache_key]

        else:
            # 2️. Decide how to call AI (ONLY ONCE)
            if not parsed["functions"] and not parsed["classes"]:
                explanation = generate_file_documentation(
                    file_path=file_path,
                    functions=[],
                    classes=[],
                    code_snippet=code[:800],
                )
            else:
                explanation = generate_file_documentation(
                    file_path=file_path,
                    functions=parsed["functions"],
                    classes=parsed["classes"],
                    code_snippet=code[:1500],
                )

            # 3️. Save to cache
            _DOC_CACHE[cache_key] = explanation

        # 4️. Append result
        docs.append({
            "file": file_path,
            "functions": parsed["functions"],
            "classes": parsed["classes"],
            "documentation": explanation,
        })

    return docs


from services.readme_service import build_readme

def generate_readme_for_repo(owner: str, repo: str, limit: int = 10):
    docs = generate_docs_for_repo(owner, repo, limit=limit)
    readme = build_readme(repo_name=repo, docs=docs)
    return readme
