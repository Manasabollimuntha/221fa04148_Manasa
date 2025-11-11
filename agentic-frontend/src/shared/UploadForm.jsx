import React, { useState } from "react";
import api from "../utils/api";

export default function UploadForm() {
  const [file, setFile] = useState(null);
  const [summary, setSummary] = useState("");
  const [loading, setLoading] = useState(false);

  const upload = async (e) => {
    e.preventDefault();
    if (!file) return;
    const form = new FormData();
    form.append("file", file);
    setLoading(true);
    try {
      const res = await api.post("/ai/upload", form, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      setSummary(res.data.parsed_summary);
    } catch (err) {
      setSummary("Failed to process document");
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <form onSubmit={upload} className="flex gap-2 items-center">
        <input type="file" onChange={(e) => setFile(e.target.files[0])} />
        <button
          className="bg-indigo-600 text-white px-3 py-1 rounded"
          disabled={loading}
        >
          {loading ? "Processing..." : "Upload"}
        </button>
      </form>
      {summary && (
        <div className="mt-4 p-3 bg-gray-100 rounded text-sm">{summary}</div>
      )}
    </>
  );
}
