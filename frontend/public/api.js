// Always use the same origin that served the page (https://news.longweingor.dev)
const API_BASE = window.location.origin + "/api";

console.log("API_BASE in api.js =", API_BASE);

async function fetchArticles(limit = 100) {
  const url = `${API_BASE}/articles?limit=${encodeURIComponent(limit)}`;
  console.log("Requesting URL:", url);

  const res = await fetch(url);

  if (!res.ok) {
    throw new Error(`Failed to fetch articles: HTTP ${res.status}`);
  }

  return res.json();
}
