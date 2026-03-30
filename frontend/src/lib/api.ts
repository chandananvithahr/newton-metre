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
