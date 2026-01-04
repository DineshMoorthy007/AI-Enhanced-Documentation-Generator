# AI-Enhanced Documentation Generator

An AI-powered tool that automatically generates high-quality technical documentation from GitHub repositories or individual source files.  
Built to help developers understand, document, and share code efficiently using structured AI prompts and code analysis.

---

## 🚀 Features

### 📦 Repository-Level Documentation
- Generate a complete `README.md` from a GitHub repository URL
- File-by-file explanations
- Extracted functions and classes
- Professional, GitHub-ready structure
- Downloadable README

### 📄 Single-File Documentation
- Paste source code and generate documentation
- Upload a source file (`.js`, `.ts`, `.py`, etc.)
- AI-generated explanations focused on purpose and responsibilities
- Export documentation as a **single-file README**

### 🤖 AI-Powered
- Role-based prompting (senior engineer style)
- Concise, structured output
- No code repetition
- Reduced hallucinations using parsing + guardrails

---

## 🧠 How It Works

1. **Input**
   - GitHub repository URL  
   - Paste code or upload a source file  

2. **Processing**
   - Repository file tree extraction
   - Function & class parsing
   - AI-driven explanation generation

3. **Output**
   - Structured README preview
   - Downloadable `README.md`
   - Clean Markdown formatting

---

## 🏗️ Project Architecture

```
AI-Enhanced-Documentation-Generator/
│
├── backend/
│   ├── main.py                 # FastAPI entry point
│   ├── requirements.txt        # Python dependencies
│   │
│   ├── api/
│   │   └── routes.py           # API endpoints
│   │
│   ├── config/
│   │   └── file_filter.json    # File filtering configuration
│   │
│   ├── models/
│   │   └── schemas.py          # Request & response models (Pydantic)
│   │
│   └── services/
│       ├── ai_service.py       # LLM interaction
│       ├── doc_service.py      # Documentation generation logic
│       ├── github_service.py   # GitHub repo validation & file fetching
│       ├── parser_service.py   # Code parsing logic
│       └── readme_service.py   # README generation service
│
├── frontend/
│   ├── public/                 # Static assets
│   ├── src/
│   │   ├── App.jsx             # Main UI logic
│   │   ├── index.css           # Tailwind styles
│   │   └── main.jsx            # Application entry point
│   │
│   ├── eslint.config.js        # ESLint configuration
│   ├── index.html              # HTML template
│   ├── package.json            # Node dependencies
│   ├── postcss.config.js       # PostCSS configuration
│   ├── tailwind.config.js      # Tailwind CSS configuration
│   └── vite.config.js          # Vite bundler configuration
│
└── README.md
```

---

## ⚙️ Tech Stack

### Backend
- Python
- FastAPI
- OpenAI API
- AST-based parsing
- GitHub REST API

### Frontend
- React
- Vite
- Tailwind CSS
- React Markdown

---

## 🛠️ Setup & Installation

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/dineshmoorthy007/AI-Enhanced-Documentation-Generator.git
cd AI-Enhanced-Documentation-Generator
```

### 2️⃣ Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Create a `.env` file in the backend directory:
```
OPENAI_API_KEY=your_api_key_here
```

Run backend:
```bash
uvicorn main:app --reload
```

Swagger UI: http://127.0.0.1:8000/docs

### 3️⃣ Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

Frontend URL: http://localhost:5173

---

## 📥 API Endpoints

| Endpoint                       | Description                      |
| ------------------------------ | -------------------------------- |
| `/validate-repo`               | Validate GitHub repository       |
| `/generate-readme`             | Generate repo-level README       |
| `/download-readme`             | Download repo README             |
| `/generate-file-doc`           | Generate docs from pasted code   |
| `/generate-file-doc/upload`    | Generate docs from uploaded file |
| `/download-single-file-readme` | Download single-file README      |

---

## 🧪 Use Cases

- Understanding unfamiliar GitHub repositories
- Documenting legacy code
- Hackathon project documentation
- Explaining single utility files
- Learning large codebases faster

---

## 🔒 Security & Privacy

- Uploaded files are processed in-memory
- No code is stored permanently
- API keys are managed via environment variables

---

## 📌 Limitations

- Private GitHub repositories are not supported yet
- Very large files are truncated for safety
- AI output depends on code clarity

---

## 🚧 Future Enhancements

- GitHub single-file URL support
- Drag-and-drop file upload
- Creative vs structured documentation modes
- PDF / HTML export
- Authentication & rate limiting

---

## 📄 License

This project is licensed under the MIT License.