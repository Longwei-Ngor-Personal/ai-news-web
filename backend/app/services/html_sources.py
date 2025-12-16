HTML_SOURCES = [
    # Cambodia - Kiripost Tech topic page (may be JS-rendered; included for testing/logging)
    {
        "name": "Kiripost Tech",
        "url": "https://kiripost.com/topics/technology",
        "category": "sea",
        "item_selector": "a",  # placeholder; we will refine tomorrow
        "title_selector": None,
        "link_attr": "href",
        "date_selector": None,
        "date_attr": None,
        "summary_selector": None,
        "max_items": 30,
    },

    # Cambodia - Khmer Times (may block bots; included for testing/logging)
    {
        "name": "Khmer Times",
        "url": "https://www.khmertimeskh.com/category/national/",
        "category": "sea",
        "item_selector": "article a",
        "title_selector": None,
        "link_attr": "href",
        "date_selector": "time",
        "date_attr": "datetime",
        "summary_selector": None,
        "max_items": 30,
    },

    # Regional - SCMP tech (may block bots; included for testing/logging)
    {
        "name": "SCMP Tech",
        "url": "https://www.scmp.com/tech",
        "category": "sea",
        "item_selector": "a",
        "title_selector": None,
        "link_attr": "href",
        "date_selector": "time",
        "date_attr": "datetime",
        "summary_selector": None,
        "max_items": 30,
    },
]
