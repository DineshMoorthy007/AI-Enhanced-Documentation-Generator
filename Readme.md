# AI-Enhanced Documentation Generator

An AI-powered web application that automatically generates high-quality technical documentation from JavaScript/TypeScript GitHub repositories. It helps solo developers and students create professional README files and clear function-level documentation without manual effort.

---

## 🚀 Problem Statement

Writing clear and structured documentation is time-consuming and often neglected in personal projects. Many developers struggle to explain functions, classes, and overall project structure, resulting in poor or missing documentation. This tool solves that problem by analyzing a GitHub repository and generating documentation automatically using AI.

---

## ✨ Key Features

- 🔗 Accepts a GitHub repository URL as input
- 📂 Analyzes repository structure and `package.json`
- 📄 Reads all relevant JavaScript / TypeScript source files
- 🧠 Uses AI to generate:
  - A professional README.md
  - Function- and class-level explanations
- 👀 Preview documentation directly in the browser
- ⬇️ Download the generated README.md
- ⚡ Beginner-friendly, fast, and scalable MVP design

---

## 🧑‍💻 Target Users

- Solo developers
- Computer science students
- Beginners building personal or learning projects
- Developers who want clean GitHub documentation with minimal effort

---

## 🛠️ Tech Stack

### Frontend
- React (Vite)
- HTML, CSS, JavaScript
- Fetch API for backend communication

### Backend
- Python
- FastAPI
- GitHub REST API

### AI
- External Large Language Model (LLM) API
- Prompt-engineered for code understanding and documentation generation

---

## 📥 Input

- A public GitHub repository URL
- Repository must contain JavaScript (`.js`) or TypeScript (`.ts`) files

---

## 📤 Output

- Generated README.md containing:
  - Project overview
  - Installation instructions
  - Usage guide
  - Folder structure explanation
  - Key features
- Structured explanations for functions and classes
- Downloadable documentation file

---

## 🔄 System Workflow

1. User submits a GitHub repository URL
2. Backend validates the repository
3. Repository metadata (file tree) is fetched
4. Relevant `.js` / `.ts` files are filtered
5. Source code is analyzed
6. AI generates structured documentation
7. Frontend displays preview
8. User downloads the README file

---

## 📡 API Endpoints

### POST /validate-repo
Validates the GitHub repository URL and accessibility.

**Request**
```json
{
  "repo_url": "https://github.com/user/repo"
}
```

---

### POST /generate-docs
Generates documentation from the repository.

**Request**
```json
{
  "repo_url": "https://github.com/user/repo"
}
```

**Response**
```json
{
  "readme": "# Project Name\n...",
  "functions": [
    {
      "file": "src/example.js",
      "name": "exampleFunction",
      "description": "Explains what the function does"
    }
  ]
}
```

---

## 🧱 Project Architecture (Monolithic & Modular)

```
backend/
├── main.py              # FastAPI entry point
├── github_service/      # GitHub repo access & metadata
├── parser_service/      # JS/TS code parsing
├── ai_service/          # LLM integration
├── doc_service/         # README & docs generation
└── models/              # Request & response schemas
```

---

## 🧪 MVP Scope

### Included in MVP

- GitHub repo input
- JS/TS support
- README generation
- Function-level explanations
- Preview + download

### Not Included (Future Work)

- Authentication
- User accounts
- Database storage
- Multiple language support
- Custom documentation styles
- Microservices architecture

---

## 🔮 Future Enhancements

- Support for Python, Java, and other languages
- Architecture diagram generation
- CLI version of the tool
- Custom documentation styles (beginner / advanced)
- Versioned documentation
- Repo change tracking and auto-regeneration

---

## 📌 Learning Outcomes

This project demonstrates:

- Real-world backend API design
- AI prompt engineering for code understanding
- GitHub API integration
- Full-stack development with React + FastAPI
- MVP-driven product thinking

---

## 📄 License

MIT License