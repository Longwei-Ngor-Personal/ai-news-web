// Always use the same origin that served the page (https://news.longweingor.dev)
const API_BASE = window.location.origin + "/api";

console.log("API_BASE in api.js =", API_BASE);

/**
 * Fetch articles with filters.
 * opts = {
 *   limit: number,
 *   hours: number | null,
 *   perCap: number,
 *   incList: string[],
 *   excList: string[],
 *   strict: boolean
 * }
 */
async function fetchArticles(opts = {}) {
  const {
    limit = 100,
    hours = null,
    perCap = 0,
    incList = [],
    excList = [],
    strict = false,
  } = opts;

  const params = new URLSearchParams();
  params.set("limit", String(limit));

  if (hours && Number.isFinite(hours)) {
    params.set("hours", String(hours));
  }

  if (perCap && Number.isFinite(perCap)) {
    params.set("per_source_cap", String(perCap));
  }

  if (incList.length) {
    params.set("include", incList.join(","));
  }

  if (excList.length) {
    params.set("exclude", excList.join(","));
  }

  if (strict) {
    params.set("strict", "true");
  }

  const url = `${API_BASE}/articles/?${params.toString()}`;
  console.log("Requesting URL:", url);

  const res = await fetch(url);

  if (!res.ok) {
    throw new Error(`Failed to fetch articles: HTTP ${res.status}`);
  }

  return res.json();
}
async function adminFetchNow() {
  const url = `${API_BASE}/admin/fetch-now`;
  const res = await fetch(url, { method: "POST" });

  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || `Fetch failed: HTTP ${res.status}`);
  }

  return res.json();
}
