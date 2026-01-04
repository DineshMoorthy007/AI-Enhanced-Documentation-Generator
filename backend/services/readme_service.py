def build_readme(repo_name: str, docs: list) -> str:
    sections = []

    # -------------------------
    # TITLE
    # -------------------------
    sections.append(f"# {repo_name}\n")

    # -------------------------
    # OVERVIEW
    # -------------------------
    sections.append(
        "## 📖 Overview\n"
        "This repository contains source code organized into multiple modules. "
        "The documentation below provides a structured overview of the codebase, "
        "including file responsibilities, functions, and classes. "
        "This README was automatically generated using an AI-powered documentation tool.\n"
    )

    # -------------------------
    # FEATURES
    # -------------------------
    sections.append(
        "## ✨ Features\n"
        "- Automated documentation from source code\n"
        "- File-level explanations\n"
        "- Function and class summaries\n"
        "- AI-assisted analysis\n"
    )

    # -------------------------
    # PROJECT STRUCTURE
    # -------------------------
    sections.append("## 🧩 Project Structure\n")

    for item in docs:
        sections.append(f"### 📄 `{item['file']}`\n")

        # File explanation
        sections.append(
            f"{item['documentation'].strip()}\n"
        )

        # Functions
        if item["functions"]:
            sections.append("**Functions:**\n")
            for fn in item["functions"]:
                sections.append(f"- `{fn}`\n")

        # Classes
        if item["classes"]:
            sections.append("\n**Classes:**\n")
            for cls in item["classes"]:
                sections.append(f"- `{cls}`\n")

        sections.append("\n---\n")

    # -------------------------
    # GETTING STARTED
    # -------------------------
    sections.append(
        "## 🚀 Getting Started\n"
        "### Prerequisites\n"
        "- Git\n"
        "- Node.js / Python (depending on the project)\n\n"
        "### Installation\n"
        "```bash\n"
        "git clone <repository-url>\n"
        "cd <repository-name>\n"
        "```\n"
    )

    # -------------------------
    # AI GENERATION INFO
    # -------------------------
    sections.append(
        "## 🤖 Documentation Generation\n"
        "This README was generated using an AI-Enhanced Documentation Generator. "
        "The system analyzes repository structure and source code to produce "
        "clear, human-readable documentation.\n"
    )

    # -------------------------
    # LICENSE
    # -------------------------
    sections.append(
        "## 📄 License\n"
        "This project is licensed under the MIT License.\n"
    )

    return "\n".join(sections)
