const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

async function safeFetch(url: string, options?: RequestInit): Promise<Response> {
  try {
    return await fetch(url, options);
  } catch {
    throw new Error("Unable to reach the server. Please check your connection and try again.");
  }
}

async function parseErrorResponse(res: Response, fallback: string): Promise<string> {
  try {
    const body = await res.json();
    return body.detail || fallback;
  } catch {
    return fallback;
  }
}

async function getAuthHeaders(): Promise<HeadersInit> {
  const { createClient } = await import("./supabase");
  const supabase = createClient();
  let { data: { session } } = await supabase.auth.getSession();

  // getSession() doesn't refresh expired tokens — try refreshing if missing
  if (!session?.access_token) {
    const { data: refreshed } = await supabase.auth.refreshSession();
    session = refreshed.session;
  }

  if (!session?.access_token) {
    throw new Error("Not authenticated");
  }

  return {
    Authorization: `Bearer ${session.access_token}`,
  };
}

export async function extractDrawing(file: File) {
  const headers = await getAuthHeaders();
  const formData = new FormData();
  formData.append("file", file);

  const res = await safeFetch(`${API_URL}/api/extract`, {
    method: "POST",
    headers,
    body: formData,
  });

  if (!res.ok) {
    throw new Error(await parseErrorResponse(res, "Extraction failed. Please try again."));
  }

  return res.json();
}

export async function extractMultiViewDrawing(files: File[]) {
  const headers = await getAuthHeaders();
  const formData = new FormData();
  files.forEach((f) => formData.append("files", f));

  const res = await safeFetch(`${API_URL}/api/extract/multi`, {
    method: "POST",
    headers,
    body: formData,
  });

  if (!res.ok) {
    throw new Error(await parseErrorResponse(res, "Multi-view extraction failed. Please try again."));
  }

  return res.json();
}

export async function createEstimate(
  extractedData: Record<string, unknown>,
  quantity = 1,
  supplierQuote?: number,
) {
  const headers = await getAuthHeaders();

  const res = await safeFetch(`${API_URL}/api/estimate`, {
    method: "POST",
    headers: { ...headers, "Content-Type": "application/json" },
    body: JSON.stringify({
      extracted_data: extractedData,
      quantity,
      supplier_quote: supplierQuote ?? null,
    }),
  });

  if (!res.ok) {
    throw new Error(await parseErrorResponse(res, "Estimation failed. Please try again."));
  }

  return res.json();
}

export async function getEstimates() {
  const headers = await getAuthHeaders();
  const res = await safeFetch(`${API_URL}/api/estimates`, { headers });
  if (!res.ok) throw new Error("Failed to load estimates. Please refresh the page.");
  return res.json();
}

export async function getEstimate(id: string) {
  const headers = await getAuthHeaders();
  const res = await safeFetch(`${API_URL}/api/estimates/${id}`, { headers });
  if (!res.ok) throw new Error("Estimate not found.");
  return res.json();
}

export async function getUsage() {
  const headers = await getAuthHeaders();
  const res = await safeFetch(`${API_URL}/api/usage`, { headers });
  if (!res.ok) throw new Error("Failed to load usage data.");
  return res.json();
}

export async function searchSimilar(file: File) {
  const headers = await getAuthHeaders();
  const formData = new FormData();
  formData.append("file", file);

  const res = await safeFetch(`${API_URL}/api/similarity/search`, {
    method: "POST",
    headers,
    body: formData,
  });

  if (!res.ok) throw new Error("Similarity search failed. Please try again.");
  return res.json();
}

export async function getMaterialPrice(name: string) {
  const headers = await getAuthHeaders();
  const params = new URLSearchParams({ name });
  const res = await safeFetch(`${API_URL}/api/material-price?${params}`, { headers });
  if (!res.ok) throw new Error(await parseErrorResponse(res, "Failed to fetch material price."));
  return res.json() as Promise<{ name: string; price_inr: number; source: string }>;
}

export interface AssemblyComponentInput {
  name: string;
  extracted_data: Record<string, unknown>;
}

export async function createAssemblyEstimate(
  components: AssemblyComponentInput[],
  joiningMethod: string,
  numJoints: number,
  quantity: number,
) {
  const headers = await getAuthHeaders();
  const res = await safeFetch(`${API_URL}/api/estimate/assembly`, {
    method: "POST",
    headers: { ...headers, "Content-Type": "application/json" },
    body: JSON.stringify({
      components,
      joining_method: joiningMethod,
      num_joints: numJoints,
      quantity,
    }),
  });
  if (!res.ok) {
    throw new Error(await parseErrorResponse(res, "Assembly estimation failed. Please try again."));
  }
  return res.json();
}

export async function embedDrawing(file: File) {
  const headers = await getAuthHeaders();
  const formData = new FormData();
  formData.append("file", file);

  const res = await safeFetch(`${API_URL}/api/similarity/embed`, {
    method: "POST",
    headers,
    body: formData,
  });

  if (!res.ok) throw new Error("Drawing processing failed. Please try again.");
  return res.json();
}

export interface RFQLineItemResult {
  line_number: number;
  part_number: string | null;
  description: string;
  quantity: number;
  material: string | null;
  delivery_weeks: number | null;
  dimensions: Record<string, number | null>;
  suggested_processes: string[];
  unit_price_expected: number | null;
  notes: string | null;
}

export interface RFQExtractResponse {
  rfq_number: string | null;
  customer: string | null;
  date: string | null;
  document_type: string;
  line_items: RFQLineItemResult[];
  confidence: string;
  page_count: number;
}

export interface RFQLineItemEstimate {
  line_number: number;
  part_number: string | null;
  description: string;
  quantity: number;
  material: string | null;
  unit_cost: number;
  order_cost: number;
  confidence_tier: string | null;
  error: string | null;
}

export interface RFQEstimateResponse {
  line_items: RFQLineItemEstimate[];
  total_order_cost: number;
  currency: string;
}

export async function extractRFQ(file: File): Promise<RFQExtractResponse> {
  const headers = await getAuthHeaders();
  const formData = new FormData();
  formData.append("file", file);

  const res = await safeFetch(`${API_URL}/api/rfq/extract`, {
    method: "POST",
    headers,
    body: formData,
  });

  if (!res.ok) throw new Error(await parseErrorResponse(res, "RFQ extraction failed. Please try again."));
  return res.json();
}

// ── Chat API ────────────────────────────────────────────────────────────────

export interface ChatMessage {
  id: string;
  role: "user" | "assistant";
  content: string;
  created_at: string;
}

export interface ChatSession {
  id: string;
  title: string;
  estimate_id: string | null;
  updated_at: string;
  message_count: number;
}

export async function sendChatMessage(
  message: string,
  sessionId?: string,
  estimateId?: string,
): Promise<{ reply: string; session_id: string; title: string }> {
  const headers = await getAuthHeaders();
  const res = await safeFetch(`${API_URL}/api/chat`, {
    method: "POST",
    headers: { ...headers, "Content-Type": "application/json" },
    body: JSON.stringify({
      message,
      session_id: sessionId || null,
      estimate_id: estimateId || null,
    }),
  });
  if (!res.ok) throw new Error(await parseErrorResponse(res, "Chat failed. Please try again."));
  return res.json();
}

export async function getChatSessions(): Promise<ChatSession[]> {
  const headers = await getAuthHeaders();
  const res = await safeFetch(`${API_URL}/api/chat/sessions`, { headers });
  if (!res.ok) throw new Error("Failed to load chat history.");
  return res.json();
}

export async function getChatMessages(sessionId: string): Promise<{
  session: { id: string; title: string; estimate_id: string | null; summary: string | null };
  messages: ChatMessage[];
}> {
  const headers = await getAuthHeaders();
  const res = await safeFetch(`${API_URL}/api/chat/sessions/${sessionId}/messages`, { headers });
  if (!res.ok) throw new Error("Failed to load chat messages.");
  return res.json();
}

export async function deleteChatSession(sessionId: string): Promise<void> {
  const headers = await getAuthHeaders();
  const res = await safeFetch(`${API_URL}/api/chat/sessions/${sessionId}`, {
    method: "DELETE",
    headers,
  });
  if (!res.ok) throw new Error("Failed to delete chat session.");
}

// ── Agent Workflow API ─────────────────────────────────────────────────────

export type WorkflowState =
  | "created"
  | "planning"
  | "awaiting_approval"
  | "executing"
  | "completed"
  | "failed"
  | "rejected";

export type ExecutionMode = "auto" | "hitl" | "manual";

export interface WorkflowSummary {
  id: string;
  workflow_type: string;
  state: WorkflowState;
  execution_mode: ExecutionMode;
  created_at: string;
  updated_at: string;
}

export interface WorkflowDetail {
  workflow_id: string;
  workflow_type: string;
  state: WorkflowState;
  execution_mode: ExecutionMode;
  inputs: Record<string, unknown>;
  outputs: Record<string, unknown>;
  created_at: string;
  updated_at: string;
}

export interface WorkflowTypeInfo {
  type: string;
  steps: string[];
}

export async function getWorkflowTypes(): Promise<WorkflowTypeInfo[]> {
  const headers = await getAuthHeaders();
  const res = await safeFetch(`${API_URL}/api/agent/workflows/types`, { headers });
  if (!res.ok) throw new Error("Failed to load workflow types.");
  const data = await res.json();
  return data.workflows;
}

export async function createWorkflow(
  workflowType: string,
  inputs: Record<string, unknown> = {},
  executionMode: ExecutionMode = "hitl",
): Promise<{ workflow_id: string; state: WorkflowState; outputs: Record<string, unknown> }> {
  const headers = await getAuthHeaders();
  const res = await safeFetch(`${API_URL}/api/agent/workflows`, {
    method: "POST",
    headers: { ...headers, "Content-Type": "application/json" },
    body: JSON.stringify({
      workflow_type: workflowType,
      inputs,
      execution_mode: executionMode,
    }),
  });
  if (!res.ok) throw new Error(await parseErrorResponse(res, "Failed to create workflow."));
  return res.json();
}

export async function getWorkflow(workflowId: string): Promise<WorkflowDetail> {
  const headers = await getAuthHeaders();
  const res = await safeFetch(`${API_URL}/api/agent/workflows/${workflowId}`, { headers });
  if (!res.ok) throw new Error("Workflow not found.");
  return res.json();
}

export async function listWorkflows(
  state?: WorkflowState,
  limit = 20,
): Promise<WorkflowSummary[]> {
  const headers = await getAuthHeaders();
  const params = new URLSearchParams();
  if (state) params.set("state", state);
  params.set("limit", String(limit));
  const res = await safeFetch(`${API_URL}/api/agent/workflows?${params}`, { headers });
  if (!res.ok) throw new Error("Failed to load workflows.");
  const data = await res.json();
  return data.workflows;
}

export async function approveWorkflow(
  workflowId: string,
  modifications?: Record<string, unknown>,
): Promise<{ workflow_id: string; state: WorkflowState; outputs: Record<string, unknown> }> {
  const headers = await getAuthHeaders();
  const res = await safeFetch(`${API_URL}/api/agent/workflows/${workflowId}/approve`, {
    method: "POST",
    headers: { ...headers, "Content-Type": "application/json" },
    body: JSON.stringify({ modifications: modifications ?? null }),
  });
  if (!res.ok) throw new Error(await parseErrorResponse(res, "Failed to approve workflow."));
  return res.json();
}

export async function rejectWorkflow(
  workflowId: string,
  reason = "",
): Promise<{ workflow_id: string; state: WorkflowState }> {
  const headers = await getAuthHeaders();
  const res = await safeFetch(`${API_URL}/api/agent/workflows/${workflowId}/reject`, {
    method: "POST",
    headers: { ...headers, "Content-Type": "application/json" },
    body: JSON.stringify({ reason }),
  });
  if (!res.ok) throw new Error(await parseErrorResponse(res, "Failed to reject workflow."));
  return res.json();
}

// ── MPN Lookup API ────────────────────────────────────────────────────────────

export async function lookupMPN(mpn: string, qty = 1) {
  const headers = await getAuthHeaders();
  const params = new URLSearchParams({ mpn, qty: String(qty) });
  const res = await safeFetch(`${API_URL}/api/mpn/lookup?${params}`, { headers });
  if (!res.ok) throw new Error(await parseErrorResponse(res, "MPN lookup failed. Check the part number and try again."));
  return res.json();
}

export async function estimateRFQ(lineItems: RFQLineItemResult[]): Promise<RFQEstimateResponse> {
  const headers = await getAuthHeaders();

  const res = await safeFetch(`${API_URL}/api/rfq/estimate`, {
    method: "POST",
    headers: { ...headers, "Content-Type": "application/json" },
    body: JSON.stringify({ line_items: lineItems }),
  });

  if (!res.ok) throw new Error(await parseErrorResponse(res, "RFQ estimation failed. Please try again."));
  return res.json();
}
