import React, { useState } from "react";
import api from "../utils/api";

export default function QAChat() {
  const [query, setQuery] = useState("");
  const [answer, setAnswer] = useState("");
  const [loading, setLoading] = useState(false);

  const ask = async () => {
    if (!query) return;
    setLoading(true);
    try {
      const res = await api.post("/ai/ask", null, { params: { query } });
      setAnswer(res.data.answer);
    } catch {
      setAnswer("Error fetching answer");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <div className="flex gap-2">
        <input
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Ask about fees, payments..."
          className="flex-1 p-2 border rounded"
        />
        <button
          onClick={ask}
          className="bg-indigo-600 text-white px-3 py-1 rounded"
          disabled={loading}
        >
          Ask
        </button>
      </div>
      {answer && <p className="mt-3 bg-gray-100 p-3 rounded text-sm">{answer}</p>}
    </div>
  );
}
