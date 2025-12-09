const API_BASE = "http://localhost:8000"; // change to your VPS domain/IP later

async function fetchArticles(limit = 50) {
  const res = await fetch(`${API_BASE}/articles?limit=${limit}`);
  if (!res.ok) {
    throw new Error(`Failed to fetch articles: ${res.status}`);
  }
  return res.json();
}
