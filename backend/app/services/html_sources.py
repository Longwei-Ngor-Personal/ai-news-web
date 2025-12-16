HTML_SOURCES = [
    # SCMP Tech – good results, but must filter out nav links
    {
        "name": "SCMP Tech",
        "url": "https://www.scmp.com/tech",
        "category": "sea",
        "item_selector": "article",          # tighter than "a"
        "title_selector": "a",               # fallback handled in code
        "link_attr": "href",
        "date_selector": "time",
        "date_attr": "datetime",
        "summary_selector": None,
        "max_items": 40,

        # SCMP articles typically contain /article/ in URL
        "include_url_regex": [r"^https?://www\.scmp\.com/.*/article/\d+"],
        "exclude_url_regex": [
            r"/rss", r"/newsletters", r"/mynews", r"/subscription", r"/privacy", r"/terms"
        ],
    },

    # Khmer Times – your previous URL may return nothing (layout/blocks).
    # Use the technology tag page (often more consistent for tech items).
    {
        "name": "Khmer Times - Technology",
        "url": "https://www.khmertimeskh.com/tag/technology/",
        "category": "sea",
        "item_selector": "article",          # tighter than "article a"
        "title_selector": "h3 a, h2 a, a",
        "link_attr": "href",
        "date_selector": "time",
        "date_attr": "datetime",
        "summary_selector": "p",
        "max_items": 40,

        # Khmer Times article URLs often contain a large numeric id like /501799919/...
        "include_url_regex": [r"^https?://www\.khmertimeskh\.com/\d{6,}/"],
        "exclude_url_regex": [
            r"/category/", r"/tag/", r"/videos/", r"/author/", r"/privacy", r"/terms"
        ],
    },
]
