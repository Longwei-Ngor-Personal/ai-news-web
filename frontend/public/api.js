// We are serving the frontend and backend on the same domain.
// So we can use a relative base URL:
const API_BASE = "/api";

async function fetchArticles(limit = 100) {
  const url = `${API_BASE}/articles?limit=${encodeURIComponent(limit)}`;
  const res = await fetch(url);

  if (!res.ok) {
    throw new Error(`Failed to fetch articles: HTTP ${res.status}`);
  }

  return res.json();
}
console.log("API_BASE =", API_BASE);
