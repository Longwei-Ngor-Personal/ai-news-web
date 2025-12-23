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
        "name": "The Hindu – Technology",
        "url": "https://www.thehindu.com/sci-tech/technology/feeder/default.rss",
        "category": "asia",
    },
    {
        "name": "Bangkok Post",
        "url": "https://www.bangkokpost.com/rss/data/technology.xml",
        "category": "asia",
    },
    {
        "name": "CGTN Sci-Tech",
        "url": "https://www.cgtn.com/feeds/rss/sci-tech.xml",
        "category": "science_tech_news"
    },
    {
        "name": "Xinhua China Science",
        "url": "http://www.xinhuanet.com/english/rss/china.xml",
        "category": "science_news"
    },
    {
        "name": "Japan Times Tech",
        "url": "https://www.japantimes.co.jp/feed/",
        "category": "tech_news"
    },
    {
        "name": "Yonhap News Agency (YNA)",
        "url": "https://en.yna.co.kr/RSS/news.xml",
        "category": "general_news"
    },
    {
        "name": "Borneo Bulletin",
        "url": "https://borneobulletin.com.bn/feed/",
        "category": "general_news"
    },
    {
        "name": "BruDirect",
        "url": "https://brudirect.com/news/rss",
        "category": "general_news"
    },
    {
        "name": "RTB News",
        "url": "https://www.rtbnews.rtb.gov.bn/RSS",
        "category": "general_news"
    },
    {
        "name": "The Scoop (Brunei)",
        "url": "https://thescoop.co/feed/",
        "category": "general_news"
    },
    {
        "name": "The Bruneian",
        "url": "https://thebruneian.news/feed/",
        "category": "general_news"
    },
    {
        "name": "Fresh News (EN)",
        "url": "https://en.freshnewsasia.com/index.php/en/rss.html",
        "category": "general_news"
    },
    {
        "name": "Phnom Penh Post",
        "url": "https://www.phnompenhpost.com/rss.xml",
        "category": "general_news"
    },
    {
        "name": "Cambodianess",
        "url": "https://cambodianess.com/rss",
        "category": "general_news"
    },
    {
        "name": "B2B Cambodia",
        "url": "https://b2b-cambodia.com/rss",
        "category": "business_news"
    },
    {
        "name": "Liputan6 News",
        "url": "https://www.liputan6.com/rss",
        "category": "general_news"
    },
    {
        "name": "Katadata Digital",
        "url": "https://katadata.co.id/rss",
        "category": "business_tech_news"
    },
    {
        "name": "Tech in Asia (Indonesia)",
        "url": "https://www.techinasia.com/tag/indonesia/feed",
        "category": "tech_media"
    },
    {
        "name": "Fintech News Indonesia",
        "url": "https://fintechnews.sg/category/indonesia/feed/",
        "category": "fintech_news"
    },
    {
        "name": "Laotian Times",
        "url": "https://laotiantimes.com/feed/",
        "category": "general_news"
    },
    {
        "name": "Vientiane Times",
        "url": "https://www.vientianetimes.org.la/rss.xml",
        "category": "general_news"
    },
    {
        "name": "KPL Laos",
        "url": "http://kpl.gov.la/En/rss.aspx",
        "category": "government_news"
    },
    {
        "name": "The Star",
        "url": "https://www.thestar.com.my/rss/",
        "category": "general_news"
    },
    {
        "name": "New Straits Times",
        "url": "https://www.nst.com.my/rss",
        "category": "general_news"
    },
    {
        "name": "Malay Mail",
        "url": "https://www.malaymail.com/rss",
        "category": "general_news"
    },
    {
        "name": "Free Malaysia Today",
        "url": "https://www.freemalaysiatoday.com/feed/",
        "category": "general_news"
    },
    {
        "name": "The Edge Malaysia",
        "url": "https://www.theedgemarkets.com/rss",
        "category": "business_news"
    },
    {
        "name": "BERNAMA",
        "url": "https://www.bernama.com/en/rss.php",
        "category": "wire_news"
    },
    {
        "name": "The Irrawaddy",
        "url": "https://www.irrawaddy.com/feed",
        "category": "general_news"
    },
    {
        "name": "Frontier Myanmar",
        "url": "https://www.frontiermyanmar.net/en/feed/",
        "category": "investigative_news"
    },
    {
        "name": "Mizzima (EN)",
        "url": "https://mizzima.com/rss.xml",
        "category": "general_news"
    },
    {
        "name": "Myanmar Now",
        "url": "https://myanmar-now.org/en/rss",
        "category": "general_news"
    },
    {
        "name": "Inquirer Tech",
        "url": "https://technology.inquirer.net/feed",
        "category": "tech_news"
    },
    {
        "name": "Philippine Star",
        "url": "https://www.philstar.com/rss",
        "category": "general_news"
    },
    {
        "name": "Manila Times",
        "url": "https://www.manilatimes.net/feed/",
        "category": "general_news"
    },
    {
        "name": "Mothership",
        "url": "https://mothership.sg/feed/",
        "category": "general_news"
    },
    {
        "name": "Today Online",
        "url": "https://www.todayonline.com/rss",
        "category": "general_news"
    }

]
