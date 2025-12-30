// Grab UI elements
const statusEl = document.getElementById("status");
const tbody = document.querySelector("#newsTable tbody");
const hoursSel = document.getElementById("hours");
const maxSel = document.getElementById("max");
const perSourceSel = document.getElementById("perSource");
const strictEl = document.getElementById("strict");
const feedlog = document.getElementById("feedlog"); // may be null if not in HTML
const kwIncEl = document.getElementById("kwInclude");
const kwExcEl = document.getElementById("kwExclude");
const feedStatusTbody = document.querySelector("#feedStatusTable tbody");

// -------------------------
// Preset definitions
// -------------------------
const PRESETS = {
  ai_balanced: {
    include: [
      "ai",
      "artificial intelligence",
      "generative ai",
      "genai",
      "llm",
      "large language model",
      "machine learning",
      "deep learning",
      "foundation model",
      "transformer",
      "inference",
      "fine-tuning",
      "rag",
      "openai",
      "anthropic",
      "claude",
      "gemini",
      "copilot",
      "chatgpt"
    ].join(", "),
    exclude: [
      "crypto",
      "bitcoin",
      "ethereum",
      "nft",
      "coupon",
      "deal",
      "discount",
      "review",
      "buy",
      "smartphone",
      "phone",
      "gaming",
      "celebrity",
      "sponsored",
      "giveaway",
      "lottery",
      "price",
      "stock",
      "earnings",
      "job",
      "hiring",
      "internship"
    ].join(", "),
    strict: true,
    perSourceCap: 5,
    hours: 48,
    limit: 80
  },

  ai_policy: {
    include: [
      "ai act",
      "regulation",
      "governance",
      "policy",
      "standards",
      "safety",
      "risk",
      "compliance",
      "audit",
      "oversight",
      "responsible ai"
    ].join(", "),
    exclude: [
      "crypto",
      "coupon",
      "deal",
      "review",
      "buy",
      "smartphone",
      "gaming",
      "celebrity",
      "sponsored",
      "job",
      "hiring"
    ].join(", "),
    strict: true,
    perSourceCap: 5,
    hours: 168,
    limit: 80
  },

  ai_research: {
    include: [
      "paper",
      "preprint",
      "arxiv",
      "benchmark",
      "evaluation",
      "model",
      "dataset",
      "inference",
      "fine-tuning",
      "training",
      "alignment",
      "transformer",
      "multimodal"
    ].join(", "),
    exclude: [
      "crypto",
      "coupon",
      "deal",
      "review",
      "buy",
      "smartphone",
      "gaming",
      "celebrity",
      "sponsored",
      "stock",
      "earnings"
    ].join(", "),
    strict: true,
    perSourceCap: 5,
    hours: 168,
    limit: 80
  }
};

function $(id) {
  return document.getElementById(id);
}

/**
 * Applies a preset to the filter inputs WITHOUT preventing users from editing afterward.
 * It simply sets default values into the boxes and toggles.
 */
function applyPreset(presetKey) {
  if (!presetKey || presetKey === "none") return;

  const preset = PRESETS[presetKey];
  if (!preset) return;

  // These IDs MATCH your actual HTML + JS bindings
  if (kwIncEl) kwIncEl.value = preset.include;
  if (kwExcEl) kwExcEl.value = preset.exclude;

  if (strictEl) strictEl.checked = !!preset.strict;
  if (hoursSel) hoursSel.value = String(preset.hours);
  if (maxSel) maxSel.value = String(preset.limit);
  if (perSourceSel) perSourceSel.value = String(preset.perSourceCap);
}


// Helpers
function dstr(d) {
  if (!d) return "";
  return new Date(d).toLocaleDateString("en-CA", { timeZone: TZ }); 
  // en-CA gives YYYY-MM-DD format
}

const TZ = "Asia/Phnom_Penh";

function fmt(dt) {
  if (!dt) return "–";
  return new Date(dt).toLocaleString("en-GB", {
    timeZone: TZ,
    hour12: false,
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
  });
}

function sanitizeUrl(u) {
  try {
    const url = new URL(u, window.location.href);
    if (url.protocol === "http:" || url.protocol === "https:") return url.href;
  } catch (e) {}
  return "";
}

function parseList(raw) {
  return (raw || "")
    .split(",")
    .map((s) => s.trim().toLowerCase())
    .filter(Boolean);
}

function setFeedlog(msg) {
  if (feedlog) feedlog.textContent = msg;
}

function getNextScheduledFetch() {
  // Make a Date object representing "now" in Phnom Penh time
  const now = new Date();
  const localNow = new Date(now.toLocaleString("en-US", { timeZone: TZ }));

  const slots = [0, 8, 16];

  for (const h of slots) {
    const candidate = new Date(localNow);
    candidate.setHours(h, 0, 0, 0);
    if (candidate > localNow) return candidate;
  }

  // Otherwise next run is tomorrow at 00:00
  const next = new Date(localNow);
  next.setDate(next.getDate() + 1);
  next.setHours(0, 0, 0, 0);
  return next;
}

// Rendering
function renderTable(items, statusText = "ok") {
  statusEl.textContent = statusText;
  tbody.innerHTML = "";

  if (!items.length) {
    const tr = document.createElement("tr");
    const td = document.createElement("td");
    td.colSpan = 4;
    td.textContent =
      "No articles available for this window/keywords. Try widening lookback or adjusting filters.";
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

// Main load function – now passes filters to backend
async function loadFromBackend() {
  const max = parseInt(maxSel.value, 10) || 100;
  const hours = parseInt(hoursSel.value, 10) || null;
  const perCap = parseInt(perSourceSel.value, 10) || 0;
  const incList = parseList(kwIncEl.value);
  const excList = parseList(kwExcEl.value);
  const strict = !!strictEl.checked;

  console.log("Filters:", { max, hours, perCap, incList, excList, strict });

  statusEl.textContent = "loading…";
  tbody.innerHTML = "";
  setFeedlog(
    "Backend is fetching from the database with your filters (time window, keywords, per-source cap)."
  );

  try {
    const articles = await fetchArticles({
      limit: max,
      hours,
      perCap,
      incList,
      excList,
      strict,
    });
    renderTable(articles, `ok (${articles.length})`);
  } catch (err) {
    console.error(err);
    statusEl.textContent = "error";
    const tr = document.createElement("tr");
    const td = document.createElement("td");
    td.colSpan = 4;
    td.textContent = `Error loading articles from backend: ${err.message}`;
    tr.appendChild(td);
    tbody.appendChild(tr);
  }
}

document.getElementById("adminFetchBtn").addEventListener("click", async () => {
  try {
    statusEl.textContent = "Running admin fetch…";
    const result = await adminFetchNow();
    statusEl.textContent = `Fetch complete: ${result.result.inserted} inserted (${result.result.skipped_existing} skipped)`;
  } catch (err) {
    statusEl.textContent = "Admin fetch error";
    alert(err.message);
  }
});

function renderFeedStatus(rows) {
  feedStatusTbody.innerHTML = "";

  if (!rows.length) {
    const tr = document.createElement("tr");
    const td = document.createElement("td");
    td.colSpan = 7;
    td.textContent = "No feed status logs yet.";
    tr.appendChild(td);
    feedStatusTbody.appendChild(tr);
    return;
  }

  rows.forEach((row) => {
    const tr = document.createElement("tr");

    const tdName = document.createElement("td");
    const a = document.createElement("a");
    a.textContent = row.feed_name;
    a.href = row.feed_url;
    a.target = "_blank";
    a.rel = "noopener";
    tdName.appendChild(a);

    const tdStatus = document.createElement("td");
    tdStatus.textContent = row.last_status || "-";

    const tdLastFetch = document.createElement("td");
    tdLastFetch.textContent = row.last_started_at ? fmt(row.last_started_at) : "-";

    const tdItems = document.createElement("td");
    tdItems.textContent =
      row.last_items_fetched != null ? String(row.last_items_fetched) : "-";

    const tdInserted = document.createElement("td");
    tdInserted.textContent =
      row.last_inserted != null ? String(row.last_inserted) : "-";

    const tdTotal = document.createElement("td");
    tdTotal.textContent = String(row.total_articles || 0);

    const tdError = document.createElement("td");
    tdError.textContent = row.last_error_message || "";

    tr.appendChild(tdName);
    tr.appendChild(tdStatus);
    tr.appendChild(tdLastFetch);
    tr.appendChild(tdItems);
    tr.appendChild(tdInserted);
    tr.appendChild(tdTotal);
    tr.appendChild(tdError);

    feedStatusTbody.appendChild(tr);
  });
}

async function loadFeedStatus() {
  try {
    const rows = await fetchFeedStats();
    renderFeedStatus(rows);

    // Last fetch = most recent finished_at among all feeds
    let lastFinished = null;

    rows.forEach((r) => {
      if (r.last_finished_at) {
        const d = new Date(r.last_finished_at);
        if (!lastFinished || d > lastFinished) lastFinished = d;
      }
    });

    const lastEl = document.getElementById("lastFetchTime");
    const nextEl = document.getElementById("nextFetchTime");

    if (lastEl) lastEl.textContent = lastFinished ? fmt(lastFinished) : "–";
    if (nextEl) nextEl.textContent = fmt(getNextScheduledFetch());
  } catch (err) {
    console.error(err);
    feedStatusTbody.innerHTML = "";
    const tr = document.createElement("tr");
    const td = document.createElement("td");
    td.colSpan = 7;
    td.textContent = `Error loading feed status: ${err.message}`;
    tr.appendChild(td);
    feedStatusTbody.appendChild(tr);
  }
}


// Wire up button + auto-load
document.getElementById("fetchBtn").addEventListener("click", loadFromBackend);
document.getElementById("refreshFeedStatsBtn").addEventListener("click", loadFeedStatus);
document.addEventListener("DOMContentLoaded", () => {
  const presetSelect = $("presetSelect");
  const presetAutoApply = $("presetAutoApply");

  // Default: AI Balanced on first load (as you requested)
  if (presetSelect && presetAutoApply && presetAutoApply.checked) {
    applyPreset(presetSelect.value || "ai_balanced");
  } else if (presetSelect && !presetSelect.value) {
    presetSelect.value = "ai_balanced";
    applyPreset("ai_balanced");
  }

  // When user changes preset, populate the boxes (still editable afterward)
  if (presetSelect) {
    presetSelect.addEventListener("change", () => {
      applyPreset(presetSelect.value);
    });
  }

  // Optional: If user unchecks auto-apply, do nothing on load next time
  // (If you want persistence, we can add localStorage—still frontend-only.)
});

// Since scripts are at end of body, safe to call immediately
loadFromBackend();
loadFeedStatus();
