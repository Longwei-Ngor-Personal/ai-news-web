# # backend/app/services/rss_feeds.py

# RSS_FEEDS = [

#     # Major AI Labs & Research
#     {"name": "OpenAI", "url": "https://openai.com/blog/rss.xml", "category": "AI Research"},
#     {"name": "Google AI Blog", "url": "https://ai.googleblog.com/feeds/posts/default", "category": "AI Research"},
#     {"name": "DeepMind Blog", "url": "https://deepmind.google/blog/feed/basic.xml", "category": "AI Research"},
#     {"name": "BAIR Blog", "url": "https://bair.berkeley.edu/blog/feed.xml", "category": "AI Research"},
#     {"name": "ArXiv cs.AI", "url": "https://export.arxiv.org/rss/cs.AI", "category": "Research"},

#     # Top Tech Media & Science
#     {"name": "MIT Technology Review", "url": "https://www.technologyreview.com/feed/", "category": "Tech"},
#     {"name": "The Verge - General", "url": "https://www.theverge.com/rss/index.xml", "category": "Tech"},
#     {"name": "The Verge - AI", "url": "https://www.theverge.com/artificial-intelligence/rss/index.xml", "category": "AI"},
#     {"name": "VentureBeat AI", "url": "https://venturebeat.com/category/ai/feed/", "category": "AI Business"},
#     {"name": "TechCrunch AI", "url": "https://techcrunch.com/tag/artificial-intelligence/feed/", "category": "Tech"},
#     {"name": "ScienceDaily AI", "url": "https://www.sciencedaily.com/rss/computers_math/artificial_intelligence.xml", "category": "AI Research"},
#     {"name": "IEEE Spectrum", "url": "https://spectrum.ieee.org/rss/fulltext", "category": "Tech"},

#     # AI Business + Industry
#     {"name": "AI Business", "url": "https://aibusiness.com/rss", "category": "AI Business"},
#     {"name": "Emerj AI Research", "url": "https://emerj.com/feed/", "category": "AI Business"},
#     {"name": "Analytics Vidhya", "url": "https://www.analyticsvidhya.com/feed/", "category": "Data Science"},
#     {"name": "KDnuggets", "url": "https://www.kdnuggets.com/feed", "category": "Data Science"},
#     {"name": "Havard Business Review", "url": "https://hbr.org/feed", "category": "Business"},

#     # Public-interest news (AI Topics)
#     {"name": "BBC AI Topic", "url": "https://www.bbc.co.uk/news/topics/ce1qrvleleqt/index.xml", "category": "AI General"},
#     {"name": "The Conversation - Tech", "url": "https://theconversation.com/uk/tech/articles.atom", "category": "Tech"},

#     # Asia-Pacific – ONLY those with confirmed RSS feeds
#     {"name": "SCMP Tech", "url": "https://www.scmp.com/rss/91/feed", "category": "Asia Tech"},
#     {"name": "Khmer Times", "url": "https://www.khmertimeskh.com/feed/", "category": "Cambodia"},
#     {"name": "Bangkok Post (Tech)", "url": "https://www.bangkokpost.com/rss/data/tech.xml", "category": "Thailand"},
#     {"name": "Philippine Star", "url": "https://www.philstar.com/rss", "category": "Philippines"},
#     {"name": "Vietnam News", "url": "https://vietnamnews.vn/rss/home.rss", "category": "Vietnam"},
#     {"name": "Tuoi Tre News", "url": "https://tuoitrenews.vn/rss/home.rss", "category": "Vietnam"},
# ]
# backend/app/services/rss_feeds.py

RSS_FEEDS = [
    # --- Major AI labs & companies ---

    # Official OpenAI news feed
    {
        "name": "OpenAI",
        "url": "https://openai.com/news/rss.xml",
        "category": "ai_lab",
    },
    {
        "name": "Google AI",
        "url": "https://research.google/blog/rss/",
        "category": "ai_lab",
    },
    {
        "name": "DeepMind",
        "url": "https://deepmind.google/blog/rss.xml",
        "category": "ai_lab",
    },
    {
        "name": "Meta AI",
        "url": "https://ai.meta.com/blog/rss/",
        "category": "ai_lab",
    },
    {
        "name": "MIT News – AI",
        "url": "https://news.mit.edu/topic/artificial-intelligence/rss",
        "category": "research",
    },
    {
        "name": "Berkeley AI Research (BAIR)",
        "url": "https://bair.berkeley.edu/blog/feed.xml",
        "category": "research",
    },

    # --- AI industry & applications ---

    {
        "name": "MIT Technology Review",
        "url": "https://www.technologyreview.com/feed/",
        "category": "tech_media",
    },
    {
        "name": "VentureBeat AI",
        "url": "https://venturebeat.com/category/ai/feed/",
        "category": "tech_media",
    },
    {
        "name": "TechCrunch",
        "url": "https://techcrunch.com/feed/",
        "category": "tech_media",
    },
    {
        "name": "Wired",
        "url": "https://www.wired.com/feed/rss",
        "category": "tech_media",
    },
    {
        "name": "The Verge",
        "url": "https://www.theverge.com/rss/index.xml",
        "category": "tech_media",
    },
    {
        "name": "IEEE Spectrum",
        "url": "https://spectrum.ieee.org/rss/fulltext",
        "category": "research",
    },
    {
        "name": "Science Daily – AI",
        "url": "https://www.sciencedaily.com/rss/computers_math/artificial_intelligence.xml",
        "category": "research",
    },


    # --- AI policy, governance & society ---

    {
        "name": "OECD AI",
        "url": "https://oecd.ai/en/rss.xml",
        "category": "policy",
    },
    {
        "name": "Euractiv – AI",
        "url": "https://www.euractiv.com/topics/artificial-intelligence/feed/",
        "category": "policy",
    },
    {
        "name": "BBC News – AI",
        "url": "https://feeds.bbci.co.uk/news/technology/rss.xml",
        "category": "policy",
    },
    {
        "name": "The Guardian – AI",
        "url": "https://www.theguardian.com/technology/artificialintelligenceai/rss",
        "category": "policy",
    },
    {
        "name": "Associated Press – AI",
        "url": "https://apnews.com/hub/artificial-intelligence?rss",
        "category": "policy",
    },
    {
        "name": "Financial Times – AI",
        "url": "https://www.ft.com/artificial-intelligence?format=rss",
        "category": "policy",
    },

    # ASEAN
    {
        "name": "Channel News Asia",
        "url": "https://www.channelnewsasia.com/rssfeeds/8395884",
        "category": "asia",
    },
    {
        "name": "The Japan Times – Tech",
        "url": "https://www.japantimes.co.jp/feed/",
        "category": "asia",
    },
    {
        "name": "The Hindu – Technology",
        "url": "https://www.thehindu.com/sci-tech/technology/feeder/default.rss",
        "category": "asia",
    },
    {
        "name": "ANTARA News",
        "url": "https://en.antaranews.com/rss",
        "category": "asia",
    },
    {
        "name": "The Jakarta Post",
        "url": "https://www.thejakartapost.com/rss",
        "category": "asia",
    },
    {
        "name": "Viet Nam News",
        "url": "https://vietnamnews.vn/rss",
        "category": "asia",
    },
    {
        "name": "VN Express International",
        "url": "https://e.vnexpress.net/rss/news.rss",
        "category": "asia",
    },
    {
        "name": "Bangkok Post",
        "url": "https://www.bangkokpost.com/rss/data/technology.xml",
        "category": "asia",
    },

]
