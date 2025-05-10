'use client';

import { useState } from 'react';

export default function Home() {
  const [input, setInput] = useState('');
  const [reply, setReply] = useState('');
  const [loading, setLoading] = useState(false);

  async function ask() {
    setLoading(true);
    try {
      const res = await fetch('http://localhost:8000/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          user_input: input,
          user_id: 'demo',
          history: [],
        }),
      });
      const data = await res.json();
      setReply(data.reply);
    } catch (err) {
      setReply(`Error: ${err}`);
    } finally {
      setLoading(false);
    }
  }

  return (
      <main className="p-6 max-w-xl mx-auto">
        <h1 className="text-2xl font-bold mb-4">FinBot Chat</h1>

        <div className="mt-2 p-2 bg-red-500 text-white rounded">
          Tailwind is live!
        </div>

        <textarea
            className="w-full border p-2 rounded"
            rows={3}
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask FinBot…"
        />

        <button
            className="mt-3 bg-blue-600 text-white px-4 py-2 rounded disabled:opacity-50"
            onClick={ask}
            disabled={loading || !input.trim()}
        >
          {loading ? 'Thinking…' : 'Send'}
        </button>

        {reply && (
            <pre className="mt-4 whitespace-pre-wrap bg-gray-800 text-gray-100 p-4 rounded">
          {reply}
        </pre>
        )}
      </main>
  );
}