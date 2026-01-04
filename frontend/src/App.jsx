import { useState } from "react";
import ReactMarkdown from "react-markdown";

function App() {
  /* -------------------- REPO README STATE -------------------- */
  const [repoUrl, setRepoUrl] = useState("");
  const [repoReadme, setRepoReadme] = useState("");
  const [repoLoading, setRepoLoading] = useState(false);
  const [repoError, setRepoError] = useState("");

  /* -------------------- SINGLE FILE STATE -------------------- */
  const [mode, setMode] = useState("paste"); // paste | upload
  const [filename, setFilename] = useState("");
  const [code, setCode] = useState("");
  const [file, setFile] = useState(null);

  const [loading, setLoading] = useState(false);
  const [output, setOutput] = useState("");
  const [error, setError] = useState("");

  /* -------------------- HANDLERS -------------------- */

  const generateRepoReadme = async () => {
    if (!repoUrl) {
      setRepoError("Please enter a GitHub repository URL");
      return;
    }

    setRepoLoading(true);
    setRepoError("");
    setRepoReadme("");

    try {
      const res = await fetch("http://127.0.0.1:8000/generate-readme", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ repo_url: repoUrl }),
      });

      if (!res.ok) throw new Error("Failed to generate README");

      const data = await res.json();
      setRepoReadme(data.readme);
    } catch (err) {
      setRepoError(err.message);
    } finally {
      setRepoLoading(false);
    }
  };

  /* 🔽 BACKEND-BASED DOWNLOAD */
  const downloadRepoReadme = () => {
    window.open("http://127.0.0.1:8000/download-readme", "_blank");
  };

  const generateFromPaste = async () => {
    if (!filename || !code) {
      setError("Filename and code are required");
      return;
    }

    setLoading(true);
    setError("");
    setOutput("");

    try {
      const res = await fetch("http://127.0.0.1:8000/generate-file-doc", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ filename, code }),
      });

      if (!res.ok) throw new Error("Failed to generate documentation");

      const data = await res.json();
      setOutput(data.documentation);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const downloadSingleFileReadme = async () => {
    const res = await fetch(
      "http://127.0.0.1:8000/download-single-file-readme",
      {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ filename, code }),
      }
    );

    const blob = await res.blob();
    const url = URL.createObjectURL(blob);

    const a = document.createElement("a");
    a.href = url;
    a.download = "README.md";
    a.click();

    URL.revokeObjectURL(url);
  };

  const generateFromUpload = async () => {
    if (!file) {
      setError("Please select a file");
      return;
    }

    setLoading(true);
    setError("");
    setOutput("");

    try {
      const formData = new FormData();
      formData.append("file", file);

      const res = await fetch(
        "http://127.0.0.1:8000/generate-file-doc/upload",
        {
          method: "POST",
          body: formData,
        }
      );

      if (!res.ok) throw new Error("Failed to generate documentation");

      const data = await res.json();
      setOutput(data.documentation);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  /* -------------------- UI -------------------- */

  return (
    <div className="min-h-screen bg-slate-100 text-slate-900">
      <div className="max-w-5xl mx-auto px-6 py-12 space-y-14">

        {/* ================= HEADER ================= */}
        <header>
          <h1 className="text-4xl font-bold mb-2">
            AI-Enhanced Documentation Generator
          </h1>
          <p className="text-slate-600 text-lg">
            Generate high-quality documentation from GitHub repositories or individual source files.
          </p>
        </header>

        {/* ================= REPO README SECTION ================= */}
        <section className="bg-white border rounded-xl p-6 space-y-4">
          <h2 className="text-2xl font-semibold">
            📦 Generate README from GitHub Repository
          </h2>

          <input
            type="text"
            placeholder="https://github.com/username/repository"
            value={repoUrl}
            onChange={(e) => setRepoUrl(e.target.value)}
            className="w-full px-4 py-3 border rounded-lg"
          />

          <div className="flex gap-4 flex-wrap">
            <button
              onClick={generateRepoReadme}
              disabled={repoLoading}
              className="px-6 py-3 bg-blue-600 hover:bg-blue-500 text-white rounded-lg font-medium"
            >
              {repoLoading ? "Generating README…" : "Generate README"}
            </button>

            {repoReadme && (
              <button
                onClick={downloadRepoReadme}
                className="px-6 py-3 bg-green-600 hover:bg-green-500 text-white rounded-lg font-medium"
              >
                ⬇ Download README.md
              </button>
            )}
          </div>

          {repoError && (
            <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded-lg">
              {repoError}
            </div>
          )}

          {repoReadme && (
            <div className="prose max-w-none border-t pt-6">
              <ReactMarkdown>{repoReadme}</ReactMarkdown>
            </div>
          )}
        </section>

        {/* ================= SINGLE FILE SECTION ================= */}
        <section className="bg-white border rounded-xl p-6 space-y-6">
          <h2 className="text-2xl font-semibold">
            📄 Generate Documentation for a Single File
          </h2>

          <div className="flex gap-3">
            <button
              onClick={() => setMode("paste")}
              className={`px-4 py-2 rounded-lg border ${
                mode === "paste"
                  ? "bg-blue-600 text-white"
                  : "bg-slate-100"
              }`}
            >
              Paste Code
            </button>

            <button
              onClick={() => setMode("upload")}
              className={`px-4 py-2 rounded-lg border ${
                mode === "upload"
                  ? "bg-blue-600 text-white"
                  : "bg-slate-100"
              }`}
            >
              Upload File
            </button>
          </div>

          {mode === "paste" && (
            <div className="space-y-4">
              <input
                type="text"
                placeholder="Filename (e.g. utils.js)"
                value={filename}
                onChange={(e) => setFilename(e.target.value)}
                className="w-full px-4 py-2 border rounded-lg"
              />

              <textarea
                placeholder="Paste your source code here…"
                value={code}
                onChange={(e) => setCode(e.target.value)}
                rows={10}
                className="w-full px-4 py-3 border rounded-lg font-mono"
              />

              <button
                onClick={generateFromPaste}
                disabled={loading}
                className="px-6 py-3 bg-blue-600 hover:bg-blue-500 text-white rounded-lg font-medium"
              >
                {loading ? "Generating…" : "Generate Documentation"}
              </button>
            </div>
          )}

          {mode === "upload" && (
            <div className="space-y-6">
              {/* Hidden input */}
              <input
                id="fileInput"
                type="file"
                onChange={(e) => setFile(e.target.files[0])}
                className="hidden"
              />

              {/* Browse Button */}
              <label
                htmlFor="fileInput"
                className="inline-flex items-center gap-3 px-6 py-3 bg-white border-2 border-dashed border-blue-400 rounded-lg cursor-pointer hover:bg-blue-50 transition font-medium text-blue-700"
              >
                📁 Browse source file
              </label>

              {file && (
                <p className="text-slate-600">
                  Selected file: <strong>{file.name}</strong>
                </p>
              )}

              <div className="mt-4">
                <button
                  onClick={generateFromUpload}
                  disabled={loading}
                  className="px-6 py-3 bg-blue-600 hover:bg-blue-500 text-white rounded-lg font-medium"
                >
                  {loading ? "Generating…" : "Generate Documentation"}
                </button>
              </div>
            </div>
          )}

          {error && (
            <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded-lg">
              {error}
            </div>
          )}

          {output && (
            <div className="prose max-w-none border-t pt-6">
              <ReactMarkdown>{output}</ReactMarkdown>
            </div>
          )}

          {output && (
            <div className="flex gap-4 mt-4">
              <button
              onClick={downloadSingleFileReadme}
              className="px-6 py-3 bg-green-600 hover:bg-green-500 text-white rounded-lg font-medium"
              >
                ⬇ Download README.md
              </button>
            </div>
          )}

        </section>
      </div>
    </div>
  );
}

export default App;
