# backend/app/services/rss_feeds.py

RSS_FEEDS = [

    # Major AI Labs & Research
    {"name": "OpenAI", "url": "https://openai.com/blog/rss.xml", "category": "AI Research"},
    {"name": "Google AI Blog", "url": "https://ai.googleblog.com/feeds/posts/default", "category": "AI Research"},
    {"name": "DeepMind Blog", "url": "https://deepmind.google/blog/feed/basic.xml", "category": "AI Research"},
    {"name": "BAIR Blog", "url": "https://bair.berkeley.edu/blog/feed.xml", "category": "AI Research"},
    {"name": "ArXiv cs.AI", "url": "https://export.arxiv.org/rss/cs.AI", "category": "Research"},
    {"name": "ArXiv cs.LG", "url": "https://export.arxiv.org/rss/cs.LG", "category": "Research"},

    # Top Tech Media & Science
    {"name": "MIT Technology Review", "url": "https://www.technologyreview.com/feed/", "category": "Tech"},
    {"name": "Wired", "url": "https://www.wired.com/feed/rss", "category": "Tech"},
    {"name": "The Verge - General", "url": "https://www.theverge.com/rss/index.xml", "category": "Tech"},
    {"name": "The Verge - AI", "url": "https://www.theverge.com/artificial-intelligence/rss/index.xml", "category": "AI"},
    {"name": "VentureBeat AI", "url": "https://venturebeat.com/category/ai/feed/", "category": "AI Business"},
    {"name": "TechCrunch AI", "url": "https://techcrunch.com/tag/artificial-intelligence/feed/", "category": "Tech"},
    {"name": "ScienceDaily AI", "url": "https://www.sciencedaily.com/rss/computers_math/artificial_intelligence.xml", "category": "AI Research"},
    {"name": "IEEE Spectrum", "url": "https://spectrum.ieee.org/rss/fulltext", "category": "Tech"},

    # AI Business + Industry
    {"name": "AI Business", "url": "https://aibusiness.com/rss", "category": "AI Business"},
    {"name": "Emerj AI Research", "url": "https://emerj.com/feed/", "category": "AI Business"},
    {"name": "Analytics Vidhya", "url": "https://www.analyticsvidhya.com/feed/", "category": "Data Science"},
    {"name": "KDnuggets", "url": "https://www.kdnuggets.com/feed", "category": "Data Science"},
    {"name": "Havard Business Review", "url": "https://hbr.org/feed", "category": "Business"},

    # Public-interest news (AI Topics)
    {"name": "BBC AI Topic", "url": "https://www.bbc.co.uk/news/topics/ce1qrvleleqt/index.xml", "category": "AI General"},
    {"name": "The Conversation - Tech", "url": "https://theconversation.com/uk/tech/articles.atom", "category": "Tech"},

    # Asia-Pacific – ONLY those with confirmed RSS feeds
    {"name": "SCMP Tech", "url": "https://www.scmp.com/rss/91/feed", "category": "Asia Tech"},
    {"name": "Khmer Times", "url": "https://www.khmertimeskh.com/feed/", "category": "Cambodia"},
    {"name": "Bangkok Post (Tech)", "url": "https://www.bangkokpost.com/rss/data/tech.xml", "category": "Thailand"},
    {"name": "Philippine Star", "url": "https://www.philstar.com/rss", "category": "Philippines"},
    {"name": "Vietnam News", "url": "https://vietnamnews.vn/rss/home.rss", "category": "Vietnam"},
    {"name": "Tuoi Tre News", "url": "https://tuoitrenews.vn/rss/home.rss", "category": "Vietnam"},
]
