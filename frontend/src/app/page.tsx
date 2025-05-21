// frontend/src/page.tsx

'use client';

import { useEffect, useRef, useState, KeyboardEvent } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';

type Turn = { role: 'user' | 'bot'; text: string };

export default function ChatPage() {
  const [history, setHistory] = useState<Turn[]>([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const bottomRef = useRef<HTMLDivElement>(null);

  /* ───────────────── helpers ───────────────── */
  const scrollToBottom = () =>
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });

  const buildApiHistory = () =>
    history.map(({ role, text }) => ({
      role: role === 'bot' ? 'assistant' : 'user',
      content: text,
    }));

  /* ───────────────── effects ───────────────── */
  useEffect(scrollToBottom, [history]);

  /* ───────────────── actions ───────────────── */
  async function send() {
    const prompt = input.trim();
    if (!prompt) return;

    const userTurn: Turn = { role: 'user', text: prompt };
    setHistory((h) => [...h, userTurn]);
    setInput('');
    setLoading(true);

    try {
      const res = await fetch('http://localhost:8000/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          user_input: prompt,
          user_id: 'demo',
          history: buildApiHistory(),
        }),
      });
      const data = await res.json();
      setHistory((h) => [...h, { role: 'bot', text: data.reply }]);
    } catch (err) {
      setHistory((h) => [
        ...h,
        { role: 'bot', text: `Error: ${(err as Error).message}` },
      ]);
    } finally {
      setLoading(false);
    }
  }

  function handleKey(
    e: KeyboardEvent<HTMLTextAreaElement>,
  ) {
    if (e.key === 'Enter' && (e.metaKey || e.ctrlKey)) {
      e.preventDefault();
      send();
    }
  }

  /* ───────────────── render ───────────────── */
  return (
    <div className="flex flex-col h-dvh bg-finbot-bg text-finbot-fg">
      {/* Chat log */}
        <div className="flex flex-col h-dvh bg-finbot-bg text-finbot-fg">
          {/* ░░ Center-column wrapper  ░░ */}
          <div className="flex flex-col w-full max-w-5xl mx-auto h-full">
            {/* Chat log */}
            <div className="flex-1 overflow-y-auto p-4 space-y-4">
              {history.map((t, i) =>
                t.role === 'user' ? (
                  <div key={i} className="text-right">{t.text}</div>
                ) : (
                  <div
                    key={i}
                    className="bg-finbot-reply text-gray-100 p-4 rounded whitespace-pre-wrap leading-none"
                  >
                    <ReactMarkdown
                      remarkPlugins={[remarkGfm]}
                      components={{
                        /* ✪ NEW — style lists & skip empty bullet nodes */
                        ul: ({ node, ...props }) => (
                          <ul className="list-disc pl-6 space-y-1" {...props} />
                        ),
                        li: ({ node, ...props }: any) => {
                          const onlyWhitespace =
                            node.children.length === 1 &&
                            node.children[0].type === 'text' &&
                            !node.children[0].value.trim();

                          return onlyWhitespace ? null : <li {...props} />;
                        },
                        /* tight paragraphs */
                        p: ({ node, ...props }) => <p className="mb-1" {...props} />,
                      }}
                    >
                      {t.text.trim()}
                    </ReactMarkdown>
                  </div>
                ),
              )}
              <div ref={bottomRef} />
            </div>

            {/* Input area */}
            <div className="border-t border-zinc-800 p-4">
              <div className="flex gap-2">
                <textarea
                  className="flex-1 resize-y bg-zinc-900 text-gray-100 p-2 rounded min-h-[4rem] max-h-40"
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  placeholder="Ask FinBot… (Ctrl/⌘ + Enter to send)"
                  onKeyDown={(e) =>
                    e.key === 'Enter' && (e.metaKey || e.ctrlKey) && (e.preventDefault(), send())
                  }
                />
                <button
                  className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded disabled:opacity-50"
                  onClick={send}
                  disabled={loading || !input.trim()}
                >
                  {loading ? '...' : 'Send'}
                </button>
              </div>
            </div>
          </div>
        </div>
    </div>
  );
}