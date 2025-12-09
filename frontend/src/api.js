// Base URL for your backend API.
// - Locally:       http://localhost:8000
// - On the VPS:    http://YOUR_SERVER_IP:8000 or https://yourdomain/api
const API_BASE = "http://localhost:8000";

async function fetchArticles(limit = 100) {
  const url = `${API_BASE}/articles?limit=${encodeURIComponent(limit)}`;
  const res = await fetch(url);

  if (!res.ok) {
    throw new Error(`Failed to fetch articles: HTTP ${res.status}`);
  }

  return res.json();
}
