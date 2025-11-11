import React, { useState, useEffect } from "react";
import api from "../utils/api";

export default function RemindersPanel() {
  const [reminders, setReminders] = useState([]);
  const [title, setTitle] = useState("");
  const [message, setMessage] = useState("");
  const [sendAt, setSendAt] = useState("");

  const load = async () => {
    const res = await api.get("/parent/reminders");
    setReminders(res.data);
  };

  const create = async (e) => {
    e.preventDefault();
    await api.post("/parent/reminders", { title, message, send_at: sendAt });
    load();
    setTitle(""); setMessage(""); setSendAt("");
  };

  useEffect(() => { load(); }, []);

  return (
    <>
      <form onSubmit={create} className="flex flex-wrap gap-2 mb-4">
        <input
          placeholder="Title"
          className="border p-2 rounded flex-1"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
        />
        <input
          placeholder="Message"
          className="border p-2 rounded flex-1"
          value={message}
          onChange={(e) => setMessage(e.target.value)}
        />
        <input
          type="datetime-local"
          className="border p-2 rounded"
          value={sendAt}
          onChange={(e) => setSendAt(e.target.value)}
        />
        <button className="bg-indigo-600 text-white px-3 py-1 rounded">
          Add
        </button>
      </form>

      <div className="space-y-2">
        {reminders.map((r) => (
          <div key={r._id} className="p-3 bg-gray-50 border rounded">
            <div className="font-semibold">{r.title}</div>
            <div className="text-sm text-gray-600">{r.message}</div>
            <div className="text-xs text-gray-500">
              {new Date(r.send_at).toLocaleString()}
            </div>
          </div>
        ))}
      </div>
    </>
  );
}
