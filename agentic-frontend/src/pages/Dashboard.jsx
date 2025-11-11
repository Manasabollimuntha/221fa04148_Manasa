import React, { useState } from "react";
import { addReminder, getReminders, askAI } from "../utils/api";

export default function Dashboard() {
  const [reminders, setReminders] = useState([]);
  const [newReminder, setNewReminder] = useState("");
  const [aiInput, setAiInput] = useState("");
  const [aiResponse, setAiResponse] = useState("");

  const handleAddReminder = async () => {
    if (!newReminder.trim()) return;
    const rem = await addReminder({ title: newReminder });
    setReminders([...reminders, rem]);
    setNewReminder("");
  };

  const handleAskAI = async () => {
    if (!aiInput.trim()) return;
    setAiResponse("Thinking...");
    const res = await askAI(aiInput);
    setAiResponse(res.message || "No response.");
  };

  return (
    <div className="bg-white p-6 rounded-2xl shadow-lg">
      <h3 className="text-2xl font-bold text-blue-700 mb-6">🎓 Parent Dashboard</h3>

      {/* Reminders */}
      <div className="mb-6">
        <h4 className="text-xl font-semibold mb-3">🕒 Reminders</h4>
        <div className="flex mb-3">
          <input
            type="text"
            className="flex-grow border p-3 rounded-l-lg"
            placeholder="Add a new reminder..."
            value={newReminder}
            onChange={(e) => setNewReminder(e.target.value)}
          />
          <button
            onClick={handleAddReminder}
            className="bg-blue-700 text-white px-5 rounded-r-lg hover:bg-blue-800"
          >
            Add
          </button>
        </div>
        <ul>
          {reminders.map((r, i) => (
            <li key={i} className="p-2 bg-gray-100 rounded mb-2">
              {r.title}
            </li>
          ))}
        </ul>
      </div>

      {/* AI Assistant */}
      <div>
        <h4 className="text-xl font-semibold mb-3">🤖 AI Assistant</h4>
        <div className="flex mb-3">
          <input
            type="text"
            className="flex-grow border p-3 rounded-l-lg"
            placeholder="Ask something about finance..."
            value={aiInput}
            onChange={(e) => setAiInput(e.target.value)}
          />
          <button
            onClick={handleAskAI}
            className="bg-purple-700 text-white px-5 rounded-r-lg hover:bg-purple-800"
          >
            Ask
          </button>
        </div>
        <div className="p-4 bg-gray-100 rounded-lg min-h-[80px]">
          {aiResponse || "Ask me something about finance..."}
        </div>
      </div>
    </div>
  );
}
