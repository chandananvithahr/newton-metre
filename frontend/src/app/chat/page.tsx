"use client";

import { useState, useEffect, useRef } from "react";
import Link from "next/link";
import {
  sendChatMessage,
  getChatSessions,
  getChatMessages,
  deleteChatSession,
  ChatSession,
  ChatMessage,
} from "@/lib/api";

export default function ChatPage() {
  const [sessions, setSessions] = useState<ChatSession[]>([]);
  const [activeSessionId, setActiveSessionId] = useState<string | null>(null);
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [sessionsLoading, setSessionsLoading] = useState(true);
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLTextAreaElement>(null);

  // Load sessions on mount
  useEffect(() => {
    loadSessions();
  }, []);

  // Auto-scroll to bottom
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  // Auto-resize textarea
  useEffect(() => {
    if (inputRef.current) {
      inputRef.current.style.height = "auto";
      inputRef.current.style.height = Math.min(inputRef.current.scrollHeight, 150) + "px";
    }
  }, [input]);

  async function loadSessions() {
    try {
      const data = await getChatSessions();
      setSessions(data);
    } catch {
      // ignore
    } finally {
      setSessionsLoading(false);
    }
  }

  async function loadSession(sessionId: string) {
    setActiveSessionId(sessionId);
    try {
      const data = await getChatMessages(sessionId);
      setMessages(data.messages);
    } catch {
      setMessages([]);
    }
  }

  async function handleNewChat() {
    setActiveSessionId(null);
    setMessages([]);
    setInput("");
    inputRef.current?.focus();
  }

  async function handleSend() {
    const msg = input.trim();
    if (!msg || loading) return;

    setInput("");
    setLoading(true);

    // Optimistic: add user message
    const tempUserMsg: ChatMessage = {
      id: `temp-${Date.now()}`,
      role: "user",
      content: msg,
      created_at: new Date().toISOString(),
    };
    setMessages((prev) => [...prev, tempUserMsg]);

    try {
      const resp = await sendChatMessage(msg, activeSessionId || undefined);

      // Add assistant reply
      const assistantMsg: ChatMessage = {
        id: `resp-${Date.now()}`,
        role: "assistant",
        content: resp.reply,
        created_at: new Date().toISOString(),
      };
      setMessages((prev) => [...prev, assistantMsg]);

      // Update session
      if (!activeSessionId) {
        setActiveSessionId(resp.session_id);
      }

      // Refresh sidebar
      loadSessions();
    } catch (e) {
      // Add error message
      const errorMsg: ChatMessage = {
        id: `err-${Date.now()}`,
        role: "assistant",
        content: `Error: ${e instanceof Error ? e.message : "Something went wrong. Please try again."}`,
        created_at: new Date().toISOString(),
      };
      setMessages((prev) => [...prev, errorMsg]);
    } finally {
      setLoading(false);
    }
  }

  async function handleDelete(sessionId: string, e: React.MouseEvent) {
    e.stopPropagation();
    try {
      await deleteChatSession(sessionId);
      setSessions((prev) => prev.filter((s) => s.id !== sessionId));
      if (activeSessionId === sessionId) {
        setActiveSessionId(null);
        setMessages([]);
      }
    } catch {
      // ignore
    }
  }

  function handleKeyDown(e: React.KeyboardEvent) {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  }

  function formatTime(dateStr: string) {
    const d = new Date(dateStr);
    const now = new Date();
    const diffDays = Math.floor((now.getTime() - d.getTime()) / (1000 * 60 * 60 * 24));
    if (diffDays === 0) return d.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
    if (diffDays === 1) return "Yesterday";
    if (diffDays < 7) return d.toLocaleDateString([], { weekday: "short" });
    return d.toLocaleDateString([], { month: "short", day: "numeric" });
  }

  return (
    <div className="h-screen flex flex-col bg-[var(--color-surface)]">
      {/* Top nav */}
      <nav className="flex items-center justify-between px-6 py-3 bg-white border-b border-black/5 shrink-0">
        <div className="flex items-center gap-3">
          <button
            onClick={() => setSidebarOpen(!sidebarOpen)}
            className="p-2 rounded-lg hover:bg-[var(--color-surface-container)] transition-colors"
          >
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <path d="M3 12h18M3 6h18M3 18h18" />
            </svg>
          </button>
          <Link href="/" className="flex items-center gap-2.5 group">
            <div className="relative w-8 h-8 flex items-center justify-center">
              <div className="absolute inset-0 bg-[var(--color-brand-dark)] rounded-xl" />
              <span className="relative text-white font-mono font-bold text-xs tracking-tighter">N·m</span>
            </div>
            <span className="text-[var(--color-brand-dark)] text-lg font-semibold tracking-tight" style={{ fontFamily: "var(--font-headline)", fontStyle: "italic" }}>
              Newton-Metre
            </span>
          </Link>
        </div>
        <div className="flex items-center gap-2">
          <Link
            href="/dashboard"
            className="text-xs text-[var(--color-text-muted)] hover:text-[var(--color-text-primary)] transition-colors px-3 py-1.5"
            style={{ fontFamily: "var(--font-label)" }}
          >
            Dashboard
          </Link>
          <Link
            href="/estimate/new"
            className="text-xs text-[var(--color-text-muted)] hover:text-[var(--color-text-primary)] transition-colors px-3 py-1.5"
            style={{ fontFamily: "var(--font-label)" }}
          >
            New Estimate
          </Link>
        </div>
      </nav>

      <div className="flex flex-1 overflow-hidden">
        {/* Sidebar */}
        {sidebarOpen && (
          <aside className="w-64 bg-white border-r border-black/5 flex flex-col shrink-0">
            <div className="p-3">
              <button
                onClick={handleNewChat}
                className="w-full flex items-center gap-2 px-3 py-2.5 rounded-lg border border-black/10 hover:bg-[var(--color-surface-container-low)] transition-colors text-sm"
                style={{ fontFamily: "var(--font-body)" }}
              >
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M12 5v14M5 12h14" />
                </svg>
                New Chat
              </button>
            </div>

            <div className="flex-1 overflow-y-auto px-2 pb-3">
              {sessionsLoading ? (
                <div className="text-center py-8 text-xs text-[var(--color-text-disabled)]">Loading...</div>
              ) : sessions.length === 0 ? (
                <div className="text-center py-8 text-xs text-[var(--color-text-disabled)]" style={{ fontFamily: "var(--font-body)" }}>
                  No conversations yet
                </div>
              ) : (
                <div className="space-y-0.5">
                  {sessions.map((s) => (
                    <div
                      key={s.id}
                      onClick={() => loadSession(s.id)}
                      className={`group flex items-center justify-between px-3 py-2 rounded-lg cursor-pointer transition-colors text-sm ${
                        activeSessionId === s.id
                          ? "bg-[var(--color-surface-container)] text-[var(--color-text-primary)]"
                          : "text-[var(--color-text-secondary)] hover:bg-[var(--color-surface-container-low)]"
                      }`}
                    >
                      <div className="min-w-0 flex-1">
                        <p className="truncate text-[13px]" style={{ fontFamily: "var(--font-body)" }}>{s.title}</p>
                        <p className="text-[10px] text-[var(--color-text-muted)] mt-0.5" style={{ fontFamily: "var(--font-mono)" }}>
                          {formatTime(s.updated_at)}
                        </p>
                      </div>
                      <button
                        onClick={(e) => handleDelete(s.id, e)}
                        className="opacity-0 group-hover:opacity-100 p-1 rounded hover:bg-red-50 hover:text-red-500 transition-all"
                      >
                        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                          <path d="M3 6h18M19 6v14a2 2 0 01-2 2H7a2 2 0 01-2-2V6m3 0V4a2 2 0 012-2h4a2 2 0 012 2v2" />
                        </svg>
                      </button>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </aside>
        )}

        {/* Main chat area */}
        <main className="flex-1 flex flex-col min-w-0">
          {/* Messages */}
          <div className="flex-1 overflow-y-auto">
            {messages.length === 0 ? (
              <div className="h-full flex items-center justify-center">
                <div className="text-center max-w-md px-6">
                  <div className="w-14 h-14 bg-[var(--color-brand-dark)] rounded-2xl flex items-center justify-center mx-auto mb-5">
                    <span className="text-white font-mono font-bold text-lg tracking-tighter">N·m</span>
                  </div>
                  <h2 className="text-xl font-semibold text-[var(--color-text-primary)] mb-2" style={{ fontFamily: "var(--font-headline)" }}>
                    Manufacturing Cost Assistant
                  </h2>
                  <p className="text-sm text-[var(--color-text-description)] mb-6" style={{ fontFamily: "var(--font-body)" }}>
                    Ask about cost breakdowns, materials, processes, or get help optimizing your manufacturing costs.
                  </p>
                  <div className="grid grid-cols-2 gap-2">
                    {[
                      "Why is EN24 steel more expensive than EN8?",
                      "How does quantity affect my unit cost?",
                      "What surface treatment is cheapest for mild steel?",
                      "Compare turning vs milling costs",
                    ].map((q) => (
                      <button
                        key={q}
                        onClick={() => { setInput(q); inputRef.current?.focus(); }}
                        className="text-left px-3 py-2.5 rounded-lg border border-black/8 text-xs text-[var(--color-text-secondary)] hover:bg-[var(--color-surface-container-low)] transition-colors"
                        style={{ fontFamily: "var(--font-body)" }}
                      >
                        {q}
                      </button>
                    ))}
                  </div>
                </div>
              </div>
            ) : (
              <div className="max-w-3xl mx-auto px-4 py-6">
                {messages.map((msg) => (
                  <div key={msg.id} className={`mb-6 ${msg.role === "user" ? "flex justify-end" : ""}`}>
                    <div className={`max-w-[85%] ${msg.role === "user" ? "ml-auto" : ""}`}>
                      {msg.role === "assistant" && (
                        <div className="flex items-center gap-2 mb-1.5">
                          <div className="w-5 h-5 bg-[var(--color-brand-dark)] rounded-md flex items-center justify-center">
                            <span className="text-white text-[8px] font-mono font-bold">Nm</span>
                          </div>
                          <span className="text-[10px] text-[var(--color-text-muted)] uppercase tracking-wider" style={{ fontFamily: "var(--font-label)" }}>
                            Newton-Metre
                          </span>
                        </div>
                      )}
                      <div
                        className={`px-4 py-3 rounded-2xl text-sm leading-relaxed ${
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
                  <div className="mb-6">
                    <div className="flex items-center gap-2 mb-1.5">
                      <div className="w-5 h-5 bg-[var(--color-brand-dark)] rounded-md flex items-center justify-center">
                        <span className="text-white text-[8px] font-mono font-bold">Nm</span>
                      </div>
                      <span className="text-[10px] text-[var(--color-text-muted)] uppercase tracking-wider" style={{ fontFamily: "var(--font-label)" }}>
                        Newton-Metre
                      </span>
                    </div>
                    <div className="bg-[var(--color-surface-container-low)] px-4 py-3 rounded-2xl rounded-bl-md inline-block">
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

          {/* Input area */}
          <div className="shrink-0 border-t border-black/5 bg-white px-4 py-3">
            <div className="max-w-3xl mx-auto">
              <div className="flex items-end gap-2 bg-[var(--color-surface-container-low)] rounded-2xl px-4 py-2 border border-black/5 focus-within:border-black/15 transition-colors">
                <textarea
                  ref={inputRef}
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  onKeyDown={handleKeyDown}
                  placeholder="Ask about manufacturing costs..."
                  rows={1}
                  className="flex-1 bg-transparent outline-none text-sm text-[var(--color-text-primary)] placeholder:text-[var(--color-text-disabled)] resize-none max-h-[150px]"
                  style={{ fontFamily: "var(--font-body)" }}
                />
                <button
                  onClick={handleSend}
                  disabled={!input.trim() || loading}
                  className="shrink-0 w-8 h-8 rounded-lg bg-[var(--color-brand-dark)] text-white flex items-center justify-center disabled:opacity-30 transition-opacity hover:bg-[var(--color-brand-dark-hover)]"
                >
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5">
                    <path d="M5 12h14M12 5l7 7-7 7" />
                  </svg>
                </button>
              </div>
              <p className="text-[10px] text-[var(--color-text-disabled)] text-center mt-2" style={{ fontFamily: "var(--font-mono)" }}>
                Newton-Metre may make mistakes. Verify critical cost data independently.
              </p>
            </div>
          </div>
        </main>
      </div>
    </div>
  );
}
