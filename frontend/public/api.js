// Base URL for your backend API (behind Caddy).
// We’ll route /api/* to FastAPI.
const API_BASE = "https://news.longweingor.dev/api";

async function fetchArticles(limit = 100) {
  const url = `${API_BASE}/articles?limit=${encodeURIComponent(limit)}`;
  const res = await fetch(url);

  if (!res.ok) {
    throw new Error(`Failed to fetch articles: HTTP ${res.status}`);
  }

  return res.json();
}
