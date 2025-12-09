// Grab UI elements
const statusEl = document.getElementById("status");
const tbody = document.querySelector("#newsTable tbody");
const hoursSel = document.getElementById("hours");
const maxSel = document.getElementById("max");
const perSourceSel = document.getElementById("perSource");
const strictEl = document.getElementById("strict");
const feedlog = document.getElementById("feedlog");
const kwIncEl = document.getElementById("kwInclude");
const kwExcEl = document.getElementById("kwExclude");

// Helpers (adapted from your original app.js)
const escapeHtml = (s = "") =>
  s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");

const dstr = (d) => (d ? new Date(d).toISOString().slice(0, 10) : "");

function sanitizeUrl(u) {
  try {
    const url = new URL(u, window.location.href);
    if (url.protocol === "http:" || url.protocol === "https:") return url.href;
  } catch (e) {}
  return "";
}

// For now, these filters are UI-only.
// Later, we can pass them as query params to the backend when you add support.
function parseList(raw) {
  return (raw || "")
    .split(",")
    .map((s) => s.trim().toLowerCase())
    .filter(Boolean);
}

// Rendering logic (adapted from your renderTable)
function renderTable(items, statusText = "ok") {
  statusEl.textContent = statusText;
  tbody.innerHTML = "";

  if (!items.length) {
    const tr = document.createElement("tr");
    const td = document.createElement("td");
    td.colSpan = 4;
    td.textContent =
      "No articles available yet. Once the backend fetcher runs and stores RSS results, they will show up here.";
    tr.appendChild(td);
    tbody.appendChild(tr);
    return;
  }

  items.forEach((article, i) => {
    const tr = document.createElement("tr");

    const tdIndex = document.createElement("td");
    tdIndex.textContent = String(i + 1);

    const tdTitle = document.createElement("td");
    const a = document.createElement("a");
    const href = sanitizeUrl(article.url || "");
    a.textContent = article.title || "(untitled)";
    if (href) {
      a.href = href;
      a.target = "_blank";
      a.rel = "noopener";
    }
    tdTitle.appendChild(a);

    const tdSource = document.createElement("td");
    tdSource.textContent = article.source || "";

    const tdDate = document.createElement("td");
    tdDate.textContent = dstr(article.published_at);

    tr.appendChild(tdIndex);
    tr.appendChild(tdTitle);
    tr.appendChild(tdSource);
    tr.appendChild(tdDate);
    tbody.appendChild(tr);
  });
}

// Main load function – calls backend instead of RSS
async function loadFromBackend() {
  // Read some values (not yet wired to backend, but kept for future)
  const max = parseInt(maxSel.value, 10) || 100;
  const hours = parseInt(hoursSel.value, 10) || 6;
  const perCap = parseInt(perSourceSel.value, 10) || 0;
  const incList = parseList(kwIncEl.value);
  const excList = parseList(kwExcEl.value);
  const strict = !!strictEl.checked;

  // For now, we just log these values; later we can pass them as query params.
  console.log("Filters (UI only for now):", {
    hours,
    max,
    perCap,
    incList,
    excList,
    strict,
  });

  statusEl.textContent = "loading…";
  tbody.innerHTML = "";
  feedlog.innerHTML =
    "Fetching from backend /articles… (actual feed-by-feed status will be implemented later on the server side)";

  try {
    const articles = await fetchArticles(max);
    renderTable(articles, `ok (${articles.length})`);
  } catch (err) {
    console.error(err);
    statusEl.textContent = "error";
    tbody.innerHTML = "";
    const tr = document.createElement("tr");
    const td = document.createElement("td");
    td.colSpan = 4;
    td.textContent = `Error loading articles from backend: ${err.message}`;
    tr.appendChild(td);
    tbody.appendChild(tr);
  }
}

// Wire up the button + auto-load
document.getElementById("fetchBtn").addEventListener("click", loadFromBackend);
document.addEventListener("DOMContentLoaded", loadFromBackend);
