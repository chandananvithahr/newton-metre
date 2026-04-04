"use client";

import { useState, useRef, useEffect } from "react";
import { sendChatMessage, ChatMessage } from "@/lib/api";

const SUGGESTIONS = [
  { icon: "💰", text: "Why is EN24 more expensive than EN8?" },
  { icon: "📊", text: "How does quantity affect unit cost?" },
  { icon: "🔧", text: "Cheapest finish for mild steel?" },
  { icon: "⚙️", text: "Compare turning vs milling costs" },
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
    <aside className="w-[380px] shrink-0 h-screen flex flex-col border-l border-black/8" style={{ background: "linear-gradient(180deg, #faf8ff 0%, #f0eef8 50%, #ebe8f3 100%)" }}>

      {/* ── Header — premium feel ──────────────────────────── */}
      <div className="shrink-0 px-5 pt-5 pb-4">
        <div className="flex items-center gap-3 mb-1">
          <div className="relative w-10 h-10 flex items-center justify-center">
            <div className="absolute inset-0 rounded-xl" style={{ background: "linear-gradient(135deg, #00288e 0%, #1e40af 100%)" }} />
            <span className="relative text-white font-mono font-bold text-sm tracking-tighter">N·m</span>
          </div>
          <div>
            <h3 className="text-[15px] font-semibold text-[var(--color-text-primary)] tracking-tight" style={{ fontFamily: "var(--font-headline)", fontStyle: "italic" }}>
              Newton-Metre
            </h3>
            <p className="text-[10px] text-[var(--color-text-muted)] font-medium tracking-wide uppercase" style={{ fontFamily: "var(--font-label)" }}>
              Manufacturing Intelligence
            </p>
          </div>
        </div>
        <div className="h-px bg-gradient-to-r from-transparent via-black/10 to-transparent mt-3" />
      </div>

      {/* ── Messages ───────────────────────────────────────── */}
      <div className="flex-1 overflow-y-auto px-4 pb-4 min-h-0">
        {messages.length === 0 ? (
          <div className="h-full flex flex-col items-center justify-center px-2">
            {/* Decorative icon */}
            <div className="relative w-16 h-16 mb-5">
              <div className="absolute inset-0 rounded-2xl opacity-10" style={{ background: "linear-gradient(135deg, #00288e 0%, #1e40af 100%)" }} />
              <div className="absolute inset-0 flex items-center justify-center">
                <svg className="w-7 h-7 text-[var(--color-nm-primary)]" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.2}>
                  <path strokeLinecap="round" strokeLinejoin="round" d="M9.813 15.904L9 18.75l-.813-2.846a4.5 4.5 0 00-3.09-3.09L2.25 12l2.846-.813a4.5 4.5 0 003.09-3.09L9 5.25l.813 2.846a4.5 4.5 0 003.09 3.09L15.75 12l-2.846.813a4.5 4.5 0 00-3.09 3.09zM18.259 8.715L18 9.75l-.259-1.035a3.375 3.375 0 00-2.455-2.456L14.25 6l1.036-.259a3.375 3.375 0 002.455-2.456L18 2.25l.259 1.035a3.375 3.375 0 002.455 2.456L21.75 6l-1.036.259a3.375 3.375 0 00-2.455 2.456z" />
                </svg>
              </div>
            </div>

            <p className="text-[14px] font-medium text-[var(--color-text-primary)] mb-1 text-center" style={{ fontFamily: "var(--font-headline)", fontStyle: "italic" }}>
              What can I help with?
            </p>
            <p className="text-[12px] text-[var(--color-text-muted)] mb-6 text-center leading-relaxed" style={{ fontFamily: "var(--font-body)" }}>
              Ask about costs, materials, processes, or negotiate smarter.
            </p>

            <div className="w-full space-y-2">
              {SUGGESTIONS.map((s) => (
                <button
                  key={s.text}
                  onClick={() => { setInput(s.text); inputRef.current?.focus(); }}
                  className="w-full flex items-center gap-3 px-4 py-3 rounded-xl bg-white/70 backdrop-blur-sm border border-black/5 text-[12px] text-[var(--color-text-secondary)] hover:bg-white hover:border-black/12 hover:shadow-sm active:scale-[0.98] transition-all duration-150"
                  style={{ fontFamily: "var(--font-body)" }}
                >
                  <span className="text-base shrink-0">{s.icon}</span>
                  <span className="text-left">{s.text}</span>
                </button>
              ))}
            </div>
          </div>
        ) : (
          <div className="space-y-5">
            {messages.map((msg) => (
              <div key={msg.id} className={msg.role === "user" ? "flex justify-end" : ""}>
                <div className={`max-w-[88%] ${msg.role === "user" ? "ml-auto" : ""}`}>
                  {msg.role === "assistant" && (
                    <div className="flex items-center gap-2 mb-1.5">
                      <div className="w-5 h-5 rounded-md flex items-center justify-center" style={{ background: "linear-gradient(135deg, #00288e 0%, #1e40af 100%)" }}>
                        <span className="text-white text-[7px] font-mono font-bold">Nm</span>
                      </div>
                      <span className="text-[9px] text-[var(--color-text-muted)] uppercase tracking-wider font-medium" style={{ fontFamily: "var(--font-label)" }}>
                        Newton-Metre
                      </span>
                    </div>
                  )}
                  <div
                    className={`px-4 py-3 text-[13px] leading-relaxed ${
                      msg.role === "user"
                        ? "rounded-2xl rounded-br-md text-white shadow-sm"
                        : "rounded-2xl rounded-bl-md bg-white/80 backdrop-blur-sm border border-black/5 text-[var(--color-text-primary)] shadow-sm"
                    }`}
                    style={{
                      fontFamily: "var(--font-body)",
                      whiteSpace: "pre-wrap",
                      ...(msg.role === "user" ? { background: "linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%)" } : {}),
                    }}
                  >
                    {msg.content}
                  </div>
                </div>
              </div>
            ))}
            {loading && (
              <div>
                <div className="flex items-center gap-2 mb-1.5">
                  <div className="w-5 h-5 rounded-md flex items-center justify-center" style={{ background: "linear-gradient(135deg, #00288e 0%, #1e40af 100%)" }}>
                    <span className="text-white text-[7px] font-mono font-bold">Nm</span>
                  </div>
                </div>
                <div className="bg-white/80 backdrop-blur-sm border border-black/5 px-4 py-3 rounded-2xl rounded-bl-md inline-block shadow-sm">
                  <div className="flex gap-1.5">
                    <div className="w-2 h-2 bg-[var(--color-nm-primary)]/40 rounded-full animate-bounce" style={{ animationDelay: "0ms" }} />
                    <div className="w-2 h-2 bg-[var(--color-nm-primary)]/40 rounded-full animate-bounce" style={{ animationDelay: "150ms" }} />
                    <div className="w-2 h-2 bg-[var(--color-nm-primary)]/40 rounded-full animate-bounce" style={{ animationDelay: "300ms" }} />
                  </div>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>
        )}
      </div>

      {/* ── Input — elevated ChatGPT-style bar ─────────────── */}
      <div className="shrink-0 px-4 pb-4 pt-2">
        <div className="bg-white rounded-2xl shadow-md border border-black/8 px-4 py-3 focus-within:shadow-lg focus-within:border-[var(--color-nm-primary)]/20 transition-all duration-200">
          <div className="flex items-end gap-3">
            <textarea
              ref={inputRef}
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="Ask anything about manufacturing..."
              aria-label="Chat message"
              rows={1}
              className="flex-1 bg-transparent outline-none text-[13px] text-[var(--color-text-primary)] placeholder:text-[var(--color-text-disabled)] resize-none max-h-[150px] leading-relaxed"
              style={{ fontFamily: "var(--font-body)" }}
            />
            <button
              onClick={handleSend}
              disabled={!input.trim() || loading}
              className="shrink-0 w-9 h-9 rounded-xl text-white flex items-center justify-center disabled:opacity-20 transition-all duration-150 hover:opacity-90 active:scale-95"
              style={{ background: "linear-gradient(135deg, #00288e 0%, #1e40af 100%)" }}
              aria-label="Send message"
            >
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5">
                <path strokeLinecap="round" strokeLinejoin="round" d="M6 12L3.269 3.126A59.768 59.768 0 0121.485 12 59.77 59.77 0 013.27 20.876L5.999 12zm0 0h7.5" />
              </svg>
            </button>
          </div>
        </div>
        <p className="text-[9px] text-[var(--color-text-disabled)] text-center mt-2.5" style={{ fontFamily: "var(--font-mono)" }}>
          Powered by Gemini Flash &middot; Verify critical data independently
        </p>
      </div>
    </aside>
  );
}
