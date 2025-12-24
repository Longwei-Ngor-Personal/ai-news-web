import os
import json
import requests
from urllib.parse import urlencode
from datetime import datetime, timezone

DATA_DIR = os.environ.get("DATA_DIR", "/data")
SENT_FILE = os.path.join(DATA_DIR, "telegram_sent_urls.json")

API_BASE = os.environ.get("NEWS_API_BASE", "http://backend:8000")  # inside docker network
BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "")

# Curated preset params (match your working frontend defaults)
CURATED_PARAMS = {
    "hours": 24,
    "limit": 80,          # fetch more, then rank + pick top 10
    "per_source_cap": 5,
    "strict": "true",
    "include": ",".join([
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
        "chatgpt",
    ]),
    "exclude": ",".join([
        "crypto","bitcoin","ethereum","nft",
        "coupon","deal","discount","review","buy",
        "smartphone","phone","gaming","celebrity",
        "sponsored","giveaway","lottery",
        "price","stock","earnings",
        "job","hiring","internship",
    ]),
}

POSITIVE_TERMS = {
    "llm": 4, "large language model": 4, "foundation model": 4,
    "inference": 3, "fine-tuning": 3, "finetuning": 3, "training": 3,
    "benchmark": 3, "evaluation": 3, "alignment": 3, "safety": 3,
    "governance": 3, "regulation": 3, "policy": 3, "ai act": 4,
    "openai": 2, "anthropic": 2, "gemini": 2, "claude": 2,
    "copilot": 2, "chatgpt": 2, "transformer": 2,
}

NEGATIVE_TERMS = {
    "review": -4, "deal": -4, "discount": -4, "coupon": -4,
    "buy": -3, "smartphone": -3, "phone": -2, "gaming": -2,
    "crypto": -4, "bitcoin": -4, "nft": -4,
    "earnings": -3, "stock": -3, "price": -2,
    "job": -4, "hiring": -4, "internship": -3,
    "giveaway": -4, "sponsored": -3, "lottery": -5,
}

def load_sent_urls() -> set[str]:
    try:
        with open(SENT_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return set(data.get("urls", []))
    except FileNotFoundError:
        return set()
    except Exception:
        return set()

def save_sent_urls(urls: set[str]) -> None:
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(SENT_FILE, "w", encoding="utf-8") as f:
        json.dump({"urls": sorted(urls)}, f, ensure_ascii=False, indent=2)

def fetch_articles() -> list[dict]:
    qs = urlencode(CURATED_PARAMS)
    url = f"{API_BASE}/articles?{qs}"
    r = requests.get(url, timeout=30)
    r.raise_for_status()
    return r.json()

def score_title(title: str) -> int:
    t = (title or "").lower()
    score = 0
    for term, w in POSITIVE_TERMS.items():
        if term in t:
            score += w
    for term, w in NEGATIVE_TERMS.items():
        if term in t:
            score += w
    return score

def rank_articles(items: list[dict]) -> list[dict]:
    for it in items:
        it["_score"] = score_title(it.get("title", ""))
    # Higher score first, then newest if published_at exists
    def key(it):
        dt = it.get("published_at") or ""
        return (it.get("_score", 0), dt)
    return sorted(items, key=key, reverse=True)

def build_message(top_items: list[dict]) -> str:
    now = datetime.now(timezone.utc).astimezone().strftime("%Y-%m-%d %H:%M")
    lines = [f"AI News Digest (Top 10) — {now}", ""]
    for i, a in enumerate(top_items, start=1):
        title = a.get("title") or "(untitled)"
        src = a.get("source") or ""
        url = a.get("url") or ""
        lines.append(f"{i}. {title}")
        if src:
            lines.append(f"   — {src}")
        if url:
            lines.append(f"   {url}")
        lines.append("")
    return "\n".join(lines).strip()

def send_telegram(text: str) -> None:
    if not BOT_TOKEN or not CHAT_ID:
        raise RuntimeError("Missing TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID env vars")

    api = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": text,
        "disable_web_page_preview": True,
    }
    r = requests.post(api, json=payload, timeout=30)
    r.raise_for_status()

def main():
    sent = load_sent_urls()
    items = fetch_articles()

    # Remove already-sent URLs
    fresh = []
    for a in items:
        url = (a.get("url") or "").strip()
        if not url or url in sent:
            continue
        fresh.append(a)

    ranked = rank_articles(fresh)
    top10 = ranked[:10]

    if not top10:
        print("No new curated items to send.")
        return

    msg = build_message(top10)
    send_telegram(msg)

    # Mark sent
    for a in top10:
        u = (a.get("url") or "").strip()
        if u:
            sent.add(u)
    save_sent_urls(sent)

    print(f"Sent {len(top10)} items to Telegram.")

if __name__ == "__main__":
    main()
