"use client";

import { useState, useRef, useEffect } from "react";
import { sendChatMessage, ChatMessage } from "@/lib/api";

const SUGGESTIONS = [
  "Why is EN24 more expensive than EN8?",
  "How does quantity affect unit cost?",
  "Cheapest finish for mild steel?",
  "Compare turning vs milling costs",
];

export function ChatPanel() {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [sessionId, setSessionId] = useState<string | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLTextAreaElement>(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  useEffect(() => {
    if (inputRef.current) {
      inputRef.current.style.height = "auto";
      inputRef.current.style.height = Math.min(inputRef.current.scrollHeight, 150) + "px";
    }
  }, [input]);

  async function handleSend() {
    const msg = input.trim();
    if (!msg || loading) return;

    setInput("");
    setLoading(true);

    const tempUserMsg: ChatMessage = {
      id: `temp-${Date.now()}`,
      role: "user",
      content: msg,
      created_at: new Date().toISOString(),
    };
    setMessages((prev) => [...prev, tempUserMsg]);

    try {
      const resp = await sendChatMessage(msg, sessionId || undefined);
      const assistantMsg: ChatMessage = {
        id: `resp-${Date.now()}`,
        role: "assistant",
        content: resp.reply,
        created_at: new Date().toISOString(),
      };
      setMessages((prev) => [...prev, assistantMsg]);
      if (!sessionId) setSessionId(resp.session_id);
    } catch (e) {
      const errorMsg: ChatMessage = {
        id: `err-${Date.now()}`,
        role: "assistant",
        content: `Error: ${e instanceof Error ? e.message : "Something went wrong."}`,
        created_at: new Date().toISOString(),
      };
      setMessages((prev) => [...prev, errorMsg]);
    } finally {
      setLoading(false);
    }
  }

  function handleKeyDown(e: React.KeyboardEvent) {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  }

  return (
    <aside className="w-[380px] shrink-0 h-screen flex flex-col bg-white border-l border-black/10">

      {/* Header */}
      <div className="flex items-center gap-3 px-5 py-4 border-b border-black/5 shrink-0">
        <div className="w-9 h-9 bg-[var(--color-brand-dark)] rounded-xl flex items-center justify-center">
          <span className="text-white font-mono font-bold text-xs tracking-tighter">N·m</span>
        </div>
        <div>
          <h3 className="text-[14px] font-semibold text-[var(--color-text-primary)]" style={{ fontFamily: "var(--font-body)" }}>
            Ask Newton-Metre
          </h3>
          <p className="text-[10px] text-[var(--color-text-muted)]" style={{ fontFamily: "var(--font-mono)" }}>
            Costs, materials, processes
          </p>
        </div>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto px-5 py-4 min-h-0">
        {messages.length === 0 ? (
          <div className="h-full flex items-center justify-center">
            <div className="text-center px-2">
              <div className="w-12 h-12 bg-[var(--color-brand-dark)]/5 rounded-2xl flex items-center justify-center mx-auto mb-4">
                <svg className="w-6 h-6 text-[var(--color-brand-dark)]" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
                  <path strokeLinecap="round" strokeLinejoin="round" d="M8.625 12a.375.375 0 11-.75 0 .375.375 0 01.75 0zm0 0H8.25m4.125 0a.375.375 0 11-.75 0 .375.375 0 01.75 0zm0 0H12m4.125 0a.375.375 0 11-.75 0 .375.375 0 01.75 0zm0 0h-.375M21 12c0 4.556-4.03 8.25-9 8.25a9.764 9.764 0 01-2.555-.337A5.972 5.972 0 015.41 20.97a5.969 5.969 0 01-.474-.065 4.48 4.48 0 00.978-2.025c.09-.457-.133-.901-.467-1.226C3.93 16.178 3 14.189 3 12c0-4.556 4.03-8.25 9-8.25s9 3.694 9 8.25z" />
                </svg>
              </div>
              <p className="text-[13px] text-[var(--color-text-description)] mb-5" style={{ fontFamily: "var(--font-body)" }}>
                Ask about manufacturing costs, materials, or processes.
              </p>
              <div className="space-y-2">
                {SUGGESTIONS.map((q) => (
                  <button
                    key={q}
                    onClick={() => { setInput(q); inputRef.current?.focus(); }}
                    className="w-full text-left px-3 py-2.5 rounded-lg border border-black/8 text-[12px] text-[var(--color-text-secondary)] hover:bg-[var(--color-surface-container-low)] hover:border-black/15 transition-colors"
                    style={{ fontFamily: "var(--font-body)" }}
                  >
                    {q}
                  </button>
                ))}
              </div>
            </div>
          </div>
        ) : (
          <div className="space-y-4">
            {messages.map((msg) => (
              <div key={msg.id} className={msg.role === "user" ? "flex justify-end" : ""}>
                <div className={`max-w-[90%] ${msg.role === "user" ? "ml-auto" : ""}`}>
                  {msg.role === "assistant" && (
                    <div className="flex items-center gap-1.5 mb-1">
                      <div className="w-5 h-5 bg-[var(--color-brand-dark)] rounded-md flex items-center justify-center">
                        <span className="text-white text-[7px] font-mono font-bold">Nm</span>
                      </div>
                      <span className="text-[9px] text-[var(--color-text-muted)] uppercase tracking-wider" style={{ fontFamily: "var(--font-label)" }}>
                        Newton-Metre
                      </span>
                    </div>
                  )}
                  <div
                    className={`px-3.5 py-2.5 rounded-2xl text-[13px] leading-relaxed ${
                      msg.role === "user"
                        ? "bg-[var(--color-brand-dark)] text-white rounded-br-md"
                        : "bg-[var(--color-surface-container-low)] text-[var(--color-text-primary)] rounded-bl-md"
                    }`}
                    style={{ fontFamily: "var(--font-body)", whiteSpace: "pre-wrap" }}
                  >
                    {msg.content}
                  </div>
                </div>
              </div>
            ))}
            {loading && (
              <div>
                <div className="flex items-center gap-1.5 mb-1">
                  <div className="w-5 h-5 bg-[var(--color-brand-dark)] rounded-md flex items-center justify-center">
                    <span className="text-white text-[7px] font-mono font-bold">Nm</span>
                  </div>
                </div>
                <div className="bg-[var(--color-surface-container-low)] px-3.5 py-2.5 rounded-2xl rounded-bl-md inline-block">
                  <div className="flex gap-1.5">
                    <div className="w-2 h-2 bg-[var(--color-text-disabled)] rounded-full animate-bounce" style={{ animationDelay: "0ms" }} />
                    <div className="w-2 h-2 bg-[var(--color-text-disabled)] rounded-full animate-bounce" style={{ animationDelay: "150ms" }} />
                    <div className="w-2 h-2 bg-[var(--color-text-disabled)] rounded-full animate-bounce" style={{ animationDelay: "300ms" }} />
                  </div>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>
        )}
      </div>

      {/* Input */}
      <div className="shrink-0 border-t border-black/5 px-4 py-3 bg-white">
        <div className="flex items-end gap-2 bg-[var(--color-surface-container-low)] rounded-xl px-3.5 py-2.5 border border-black/5 focus-within:border-black/15 focus-within:shadow-sm transition-all">
          <textarea
            ref={inputRef}
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Ask about costs, materials, processes..."
            aria-label="Chat message"
            rows={1}
            className="flex-1 bg-transparent outline-none text-[13px] text-[var(--color-text-primary)] placeholder:text-[var(--color-text-disabled)] resize-none max-h-[150px]"
            style={{ fontFamily: "var(--font-body)" }}
          />
          <button
            onClick={handleSend}
            disabled={!input.trim() || loading}
            className="shrink-0 w-8 h-8 rounded-lg bg-[var(--color-brand-dark)] text-white flex items-center justify-center disabled:opacity-30 transition-all hover:bg-[var(--color-brand-dark-hover)]"
            aria-label="Send message"
          >
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5">
              <path d="M5 12h14M12 5l7 7-7 7" />
            </svg>
          </button>
        </div>
        <p className="text-[9px] text-[var(--color-text-disabled)] text-center mt-2" style={{ fontFamily: "var(--font-mono)" }}>
          May make mistakes. Verify critical data independently.
        </p>
      </div>
    </aside>
  );
}
