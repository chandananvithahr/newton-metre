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
  const {
    data: { session },
  } = await supabase.auth.getSession();

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

export async function createEstimate(extractedData: Record<string, unknown>, quantity = 1) {
  const headers = await getAuthHeaders();

  const res = await safeFetch(`${API_URL}/api/estimate`, {
    method: "POST",
    headers: { ...headers, "Content-Type": "application/json" },
    body: JSON.stringify({ extracted_data: extractedData, quantity }),
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
