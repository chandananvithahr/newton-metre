"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { embedDrawing, searchSimilar } from "@/lib/api";

interface Match {
  drawing_id: string;
  score: number;
  metadata: Record<string, unknown>;
}

export default function SimilarPartsPage() {
  const router = useRouter();
  const [files, setFiles] = useState<File[]>([]);
  const [loading, setLoading] = useState(false);
  const [step, setStep] = useState<"upload" | "results">("upload");
  const [matches, setMatches] = useState<Match[]>([]);
  const [error, setError] = useState("");

  async function handleSearch() {
    if (files.length < 2) {
      setError("Upload at least 2 drawings to compare.");
      return;
    }

    setError("");
    setLoading(true);

    try {
      for (const file of files) {
        await embedDrawing(file);
      }
      const result = await searchSimilar(files[0]);
      setMatches(result.matches);
      setStep("results");
    } catch (e) {
      setError(e instanceof Error ? e.message : "Search failed");
    }

    setLoading(false);
  }

  if (step === "upload") {
    return (
      <div className="min-h-screen bg-gray-50">
        <nav className="flex items-center justify-between px-8 py-4 bg-white border-b">
          <span className="text-xl font-bold cursor-pointer" onClick={() => router.push("/dashboard")}>Costimize</span>
        </nav>
        <div className="max-w-2xl mx-auto px-8 py-16">
          <h1 className="text-3xl font-bold mb-2">Similar Parts Search</h1>
          <p className="text-gray-600 mb-8">Upload 2 or more engineering drawings to find similar parts and compare costs.</p>

          <div className="bg-white rounded-xl shadow p-8">
            <div className="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center mb-6">
              <input
                type="file"
                accept=".pdf,.png,.jpg,.jpeg"
                multiple
                onChange={(e) => setFiles(Array.from(e.target.files || []))}
                className="mx-auto"
              />
              <p className="text-gray-500 text-sm mt-2">Select multiple files (PDF, PNG, JPG)</p>
            </div>

            {files.length > 0 && (
              <p className="text-sm text-gray-600 mb-4">
                {files.length} file(s): {files.map((f) => f.name).join(", ")}
              </p>
            )}

            {error && <p className="text-red-500 text-sm mb-4">{error}</p>}

            <button
              onClick={handleSearch}
              disabled={loading || files.length < 2}
              className="w-full bg-blue-600 text-white py-3 rounded-lg hover:bg-blue-700 disabled:opacity-50"
            >
              {loading ? "Processing..." : "Find Similar Parts"}
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <nav className="flex items-center justify-between px-8 py-4 bg-white border-b">
        <span className="text-xl font-bold cursor-pointer" onClick={() => router.push("/dashboard")}>Costimize</span>
      </nav>
      <div className="max-w-3xl mx-auto px-8 py-8">
        <h1 className="text-3xl font-bold mb-6">Similarity Results</h1>

        {matches.length === 0 ? (
          <div className="bg-white rounded-xl shadow p-8 text-center text-gray-500">
            No similar parts found. Upload more drawings to build your library.
          </div>
        ) : (
          <div className="bg-white rounded-xl shadow overflow-hidden">
            <table className="w-full">
              <thead className="bg-gray-50 border-b">
                <tr>
                  <th className="text-left px-6 py-3 text-sm font-medium text-gray-500">Drawing</th>
                  <th className="text-right px-6 py-3 text-sm font-medium text-gray-500">Similarity</th>
                </tr>
              </thead>
              <tbody className="divide-y">
                {matches.map((m) => (
                  <tr key={m.drawing_id}>
                    <td className="px-6 py-4">{(m.metadata.filename as string) || m.drawing_id}</td>
                    <td className="px-6 py-4 text-right font-mono">{(m.score * 100).toFixed(1)}%</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}

        <button
          onClick={() => { setStep("upload"); setMatches([]); setFiles([]); }}
          className="mt-6 border px-6 py-3 rounded-lg hover:bg-gray-50"
        >
          New Search
        </button>
      </div>
    </div>
  );
}
