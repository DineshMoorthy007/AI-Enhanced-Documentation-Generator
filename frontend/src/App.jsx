import { useState } from "react";
import ReactMarkdown from "react-markdown";

function App() {
  const [repoUrl, setRepoUrl] = useState("");
  const [readme, setReadme] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState(false);

  const generateDocs = async () => {
    if (!repoUrl) {
      setError("Please enter a GitHub repository URL");
      return;
    }

    setLoading(true);
    setError("");
    setReadme("");
    setSuccess(false);

    try {
      const response = await fetch("http://127.0.0.1:8000/generate-readme", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ repo_url: repoUrl }),
      });

      if (!response.ok) {
        throw new Error("Failed to generate documentation");
      }

      const data = await response.json();
      setReadme(data.readme);
      setSuccess(true);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const downloadReadme = () => {
    const blob = new Blob([readme], { type: "text/markdown" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "README.md";
    a.click();
    URL.revokeObjectURL(url);
  };
  function Spinner() {
  return (
    <div className="flex items-center gap-3 text-slate-400">
      <div className="h-5 w-5 animate-spin rounded-full border-2 border-slate-600 border-t-blue-500"></div>
      <span>Analyzing repository and generating documentation…</span>
    </div>
  );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-950 to-slate-900 text-slate-200">
      <div className="max-w-4xl mx-auto px-6 py-12 space-y-8">

        {/* HEADER */}
        <header>
          <h1 className="text-4xl font-bold mb-2">
            AI-Enhanced Documentation Generator
          </h1>
          <p className="text-slate-400 text-lg">
            Generate clean, professional README files automatically from GitHub repositories.
          </p>
        </header>

        {/* INPUT */}
        <div className="flex flex-col sm:flex-row gap-4">
          <input
            type="text"
            disabled={loading}
            placeholder="https://github.com/user/repo"
            value={repoUrl}
            onChange={(e) => setRepoUrl(e.target.value)}
            className="flex-1 px-4 py-3 rounded-lg bg-slate-900 border border-slate-700 focus:outline-none focus:ring-2 focus:ring-blue-600"
          />
          {loading && (
            <div className="mt-4">
            <Spinner />
            </div>
          )}

          <button
            onClick={generateDocs}
            disabled={loading}
            className="px-6 py-3 rounded-lg bg-blue-600 hover:bg-blue-500 disabled:bg-slate-600 transition font-medium"
          >
            {loading ? "Generating…" : "Generate"}
          </button>
        </div>

        {error && (
          <div className="bg-red-900/30 border border-red-700 text-red-300 px-4 py-3 rounded-lg">
            {error}
          </div>
        )}

        
        {success && !loading && (
          <p className="text-green-400">
            Documentation generated successfully 🎉
          </p>
        )}

        {/* README */}
        {readme && (
          <section className="bg-slate-900 border border-slate-800 rounded-xl p-8 space-y-6">
            <h2 className="text-2xl font-semibold">
              README Preview
            </h2>

            <div className="prose prose-invert max-w-none">
              <ReactMarkdown>{readme}</ReactMarkdown>
            </div>

            <button
              onClick={downloadReadme}
              className="px-6 py-3 rounded-lg bg-green-600 hover:bg-green-500 transition font-medium"
            >
              Download README.md
            </button>
          </section>
        )}

      </div>
    </div>
  );
}

export default App;
