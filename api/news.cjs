// api/news.cjs
const Parser = require("rss-parser");
const dayjs = require("dayjs");
const parser = new Parser({ timeout: 15000 });

const FEEDS = [ /* same as above */ ];

module.exports = async (req, res) => {
  try {
    const hours = Math.max(1, parseInt(req.query.hours || "48", 10));
    const max = Math.max(1, parseInt(req.query.max || "20", 10));
    let items = [];
    for (const f of FEEDS) {
      try {
        const parsed = await parser.parseURL(f.url);
        for (const e of parsed.items || []) {
          const d = e.isoDate || e.pubDate || null;
          items.push({
            title: e.title || "(untitled)",
            url: e.link || e.guid || "",
            source: f.name || parsed.title || "",
            date: d ? new Date(d).toISOString() : null
          });
        }
      } catch (err) {
        console.warn("Feed error:", f.url, err?.message);
      }
    }
    const map = new Map();
    for (const it of items) {
      const key = (it.url || "") + "|" + (it.title || "");
      const prev = map.get(key);
      if (!prev || (it.date && (!prev.date || it.date > prev.date))) map.set(key, it);
    }
    const cutoff = dayjs().subtract(hours, "hour");
    items = [...map.values()]
      .filter(it => !it.date || dayjs(it.date).isAfter(cutoff))
      .sort((a, b) => new Date(b.date || 0) - new Date(a.date || 0))
      .slice(0, max);

    res.setHeader("Cache-Control", "s-maxage=60, stale-while-revalidate=300");
    res.status(200).json({ ok: true, count: items.length, items });
  } catch (e) {
    res.status(500).json({ ok: false, error: String(e) });
  }
};
