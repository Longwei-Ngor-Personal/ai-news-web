HTML_SOURCES = [
    # ========= ENABLED (known to work / already tuned) =========

    {
        "name": "SCMP Tech",
        "url": "https://www.scmp.com/tech",
        "category": "asia",
        "enabled": True,
        "item_selector": "article",
        "title_selector": "a",
        "link_attr": "href",
        "date_selector": "time",
        "date_attr": "datetime",
        "summary_selector": None,
        "max_items": 50,
        "include_url_regex": [r"^https?://www\.scmp\.com/.*/article/\d+"],
        "exclude_url_regex": [r"/rss", r"/newsletters", r"/subscription", r"/privacy", r"/terms"],
    },

    {
        "name": "Kiripost Tech",
        "url": "https://kiripost.com/topics/technology",
        "category": "sea",
        "enabled": True,
        # Kiripost may be layout-dependent; keep broad but filter URLs
        "item_selector": "a",
        "title_selector": None,
        "link_attr": "href",
        "date_selector": None,
        "date_attr": None,
        "summary_selector": None,
        "max_items": 50,
        "include_url_regex": [r"^https?://kiripost\.com/"],
        "exclude_url_regex": [r"/topics/", r"/tag/", r"/about", r"/contact", r"/privacy", r"/terms"],
    },

    # ========= DISABLED PLACEHOLDERS (inventory only; enable after tuning) =========
    # China / East Asia
    {"name": "CGTN Sci-Tech", "url": "https://www.cgtn.com/sci-tech.html", "category": "asia", "enabled": False,
     "item_selector": "article", "title_selector": "a", "link_attr": "href", "date_selector": "time", "date_attr": "datetime",
     "summary_selector": None, "max_items": 40, "include_url_regex": [], "exclude_url_regex": []},

    {"name": "Xinhua China Science", "url": "http://www.xinhuanet.com/english/list/china-science.htm", "category": "asia", "enabled": False,
     "item_selector": "a", "title_selector": None, "link_attr": "href", "date_selector": None, "date_attr": None,
     "summary_selector": None, "max_items": 40, "include_url_regex": [], "exclude_url_regex": []},

    {"name": "Japan Times Tech", "url": "https://www.japantimes.co.jp/business/tech/", "category": "asia", "enabled": False,
     "item_selector": "article", "title_selector": "a", "link_attr": "href", "date_selector": "time", "date_attr": "datetime",
     "summary_selector": None, "max_items": 40, "include_url_regex": [], "exclude_url_regex": []},

    {"name": "Yonhap (YNA)", "url": "https://en.yna.co.kr/", "category": "asia", "enabled": False,
     "item_selector": "a", "title_selector": None, "link_attr": "href", "date_selector": "time", "date_attr": "datetime",
     "summary_selector": None, "max_items": 40, "include_url_regex": [], "exclude_url_regex": []},

    # Brunei
    {"name": "Borneo Bulletin", "url": "https://borneobulletin.com.bn/", "category": "sea", "enabled": False,
     "item_selector": "article", "title_selector": "a", "link_attr": "href", "date_selector": "time", "date_attr": "datetime",
     "summary_selector": None, "max_items": 40, "include_url_regex": [], "exclude_url_regex": []},

    {"name": "BruDirect", "url": "https://www.brudirect.com/", "category": "sea", "enabled": False,
     "item_selector": "article", "title_selector": "a", "link_attr": "href", "date_selector": "time", "date_attr": "datetime",
     "summary_selector": None, "max_items": 40, "include_url_regex": [], "exclude_url_regex": []},

    {"name": "RTB News", "url": "https://www.rtbnews.rtb.gov.bn/SitePages/Home.aspx", "category": "sea", "enabled": False,
     "item_selector": "a", "title_selector": None, "link_attr": "href", "date_selector": None, "date_attr": None,
     "summary_selector": None, "max_items": 40, "include_url_regex": [], "exclude_url_regex": []},

    {"name": "The Scoop (Brunei)", "url": "https://thescoop.co/", "category": "sea", "enabled": False,
     "item_selector": "article", "title_selector": "a", "link_attr": "href", "date_selector": "time", "date_attr": "datetime",
     "summary_selector": None, "max_items": 40, "include_url_regex": [], "exclude_url_regex": []},

    {"name": "The Bruneian", "url": "https://thebruneian.news/", "category": "sea", "enabled": False,
     "item_selector": "article", "title_selector": "a", "link_attr": "href", "date_selector": "time", "date_attr": "datetime",
     "summary_selector": None, "max_items": 40, "include_url_regex": [], "exclude_url_regex": []},

    # Cambodia (disabled until tuned / some are blocked)
    {"name": "Fresh News (EN)", "url": "https://en.freshnewsasia.com/index.php/en/", "category": "sea", "enabled": False,
     "item_selector": "a", "title_selector": None, "link_attr": "href", "date_selector": None, "date_attr": None,
     "summary_selector": None, "max_items": 40, "include_url_regex": [], "exclude_url_regex": []},

    {"name": "Phnom Penh Post", "url": "https://www.phnompenhpost.com/national", "category": "sea", "enabled": False,
     "item_selector": "article", "title_selector": "a", "link_attr": "href", "date_selector": "time", "date_attr": "datetime",
     "summary_selector": None, "max_items": 40, "include_url_regex": [], "exclude_url_regex": []},

    {"name": "Cambodianess", "url": "https://cambodianess.com/", "category": "sea", "enabled": False,
     "item_selector": "article", "title_selector": "a", "link_attr": "href", "date_selector": "time", "date_attr": "datetime",
     "summary_selector": None, "max_items": 40, "include_url_regex": [], "exclude_url_regex": []},

    {"name": "B2B Cambodia", "url": "https://b2b-cambodia.com/business/news/", "category": "sea", "enabled": False,
     "item_selector": "article", "title_selector": "a", "link_attr": "href", "date_selector": None, "date_attr": None,
     "summary_selector": None, "max_items": 40, "include_url_regex": [], "exclude_url_regex": []},

    # Indonesia
    {"name": "Liputan6 News", "url": "https://www.liputan6.com/news", "category": "sea", "enabled": False,
     "item_selector": "article", "title_selector": "a", "link_attr": "href", "date_selector": "time", "date_attr": "datetime",
     "summary_selector": None, "max_items": 40, "include_url_regex": [], "exclude_url_regex": []},

    {"name": "Katadata Digital", "url": "https://katadata.co.id/digital", "category": "sea", "enabled": False,
     "item_selector": "article", "title_selector": "a", "link_attr": "href", "date_selector": None, "date_attr": None,
     "summary_selector": None, "max_items": 40, "include_url_regex": [], "exclude_url_regex": []},

    {"name": "Tech in Asia (Indonesia tag)", "url": "https://www.techinasia.com/tag/indonesia", "category": "sea", "enabled": False,
     "item_selector": "article", "title_selector": "a", "link_attr": "href", "date_selector": "time", "date_attr": "datetime",
     "summary_selector": None, "max_items": 20, "include_url_regex": [], "exclude_url_regex": []},

    {"name": "Fintech News Indonesia", "url": "https://fintechnews.id/", "category": "sea", "enabled": False,
     "item_selector": "article", "title_selector": "a", "link_attr": "href", "date_selector": None, "date_attr": None,
     "summary_selector": None, "max_items": 30, "include_url_regex": [], "exclude_url_regex": []},

    # Laos
    {"name": "Laotian Times", "url": "https://laotiantimes.com/", "category": "sea", "enabled": False,
     "item_selector": "article", "title_selector": "a", "link_attr": "href", "date_selector": "time", "date_attr": "datetime",
     "summary_selector": None, "max_items": 30, "include_url_regex": [], "exclude_url_regex": []},

    {"name": "Vientiane Times", "url": "https://www.vientianetimes.org.la/", "category": "sea", "enabled": False,
     "item_selector": "article", "title_selector": "a", "link_attr": "href", "date_selector": None, "date_attr": None,
     "summary_selector": None, "max_items": 30, "include_url_regex": [], "exclude_url_regex": []},

    {"name": "KPL Laos", "url": "https://kpl.gov.la/EN/", "category": "sea", "enabled": False,
     "item_selector": "a", "title_selector": None, "link_attr": "href", "date_selector": None, "date_attr": None,
     "summary_selector": None, "max_items": 30, "include_url_regex": [], "exclude_url_regex": []},

    # Malaysia
    {"name": "The Star", "url": "https://www.thestar.com.my/", "category": "sea", "enabled": False,
     "item_selector": "article", "title_selector": "a", "link_attr": "href", "date_selector": "time", "date_attr": "datetime",
     "summary_selector": None, "max_items": 30, "include_url_regex": [], "exclude_url_regex": []},

    {"name": "New Straits Times", "url": "https://www.nst.com.my/", "category": "sea", "enabled": False,
     "item_selector": "article", "title_selector": "a", "link_attr": "href", "date_selector": "time", "date_attr": "datetime",
     "summary_selector": None, "max_items": 30, "include_url_regex": [], "exclude_url_regex": []},

    {"name": "Malay Mail", "url": "https://www.malaymail.com/", "category": "sea", "enabled": False,
     "item_selector": "article", "title_selector": "a", "link_attr": "href", "date_selector": "time", "date_attr": "datetime",
     "summary_selector": None, "max_items": 30, "include_url_regex": [], "exclude_url_regex": []},

    {"name": "Free Malaysia Today", "url": "https://www.freemalaysiatoday.com/", "category": "sea", "enabled": False,
     "item_selector": "article", "title_selector": "a", "link_attr": "href", "date_selector": "time", "date_attr": "datetime",
     "summary_selector": None, "max_items": 30, "include_url_regex": [], "exclude_url_regex": []},

    {"name": "The Edge Malaysia", "url": "https://theedgemalaysia.com/", "category": "sea", "enabled": False,
     "item_selector": "article", "title_selector": "a", "link_attr": "href", "date_selector": None, "date_attr": None,
     "summary_selector": None, "max_items": 30, "include_url_regex": [], "exclude_url_regex": []},

    {"name": "BERNAMA", "url": "https://www.bernama.com/en/", "category": "sea", "enabled": False,
     "item_selector": "article", "title_selector": "a", "link_attr": "href", "date_selector": None, "date_attr": None,
     "summary_selector": None, "max_items": 30, "include_url_regex": [], "exclude_url_regex": []},

    # Myanmar
    {"name": "The Irrawaddy", "url": "https://www.irrawaddy.com/", "category": "sea", "enabled": False,
     "item_selector": "article", "title_selector": "a", "link_attr": "href", "date_selector": None, "date_attr": None,
     "summary_selector": None, "max_items": 30, "include_url_regex": [], "exclude_url_regex": []},

    {"name": "Frontier Myanmar", "url": "https://www.frontiermyanmar.net/en/", "category": "sea", "enabled": False,
     "item_selector": "article", "title_selector": "a", "link_attr": "href", "date_selector": "time", "date_attr": "datetime",
     "summary_selector": None, "max_items": 30, "include_url_regex": [], "exclude_url_regex": []},

    {"name": "Mizzima (EN)", "url": "https://eng.mizzima.com/", "category": "sea", "enabled": False,
     "item_selector": "article", "title_selector": "a", "link_attr": "href", "date_selector": None, "date_attr": None,
     "summary_selector": None, "max_items": 30, "include_url_regex": [], "exclude_url_regex": []},

    {"name": "Myanmar Now", "url": "https://myanmar-now.org/en/", "category": "sea", "enabled": False,
     "item_selector": "article", "title_selector": "a", "link_attr": "href", "date_selector": None, "date_attr": None,
     "summary_selector": None, "max_items": 30, "include_url_regex": [], "exclude_url_regex": []},

    # Philippines
    {"name": "Inquirer Tech", "url": "https://technology.inquirer.net/", "category": "sea", "enabled": False,
     "item_selector": "article", "title_selector": "a", "link_attr": "href", "date_selector": "time", "date_attr": "datetime",
     "summary_selector": None, "max_items": 30, "include_url_regex": [], "exclude_url_regex": []},

    {"name": "Philippine Star", "url": "https://www.philstar.com/", "category": "sea", "enabled": False,
     "item_selector": "article", "title_selector": "a", "link_attr": "href", "date_selector": "time", "date_attr": "datetime",
     "summary_selector": None, "max_items": 30, "include_url_regex": [], "exclude_url_regex": []},

    {"name": "Manila Times", "url": "https://www.manilatimes.net/", "category": "sea", "enabled": False,
     "item_selector": "article", "title_selector": "a", "link_attr": "href", "date_selector": "time", "date_attr": "datetime",
     "summary_selector": None, "max_items": 30, "include_url_regex": [], "exclude_url_regex": []},

    # Singapore
    {"name": "Mothership", "url": "https://mothership.sg/", "category": "sea", "enabled": False,
     "item_selector": "article", "title_selector": "a", "link_attr": "href", "date_selector": "time", "date_attr": "datetime",
     "summary_selector": None, "max_items": 30, "include_url_regex": [], "exclude_url_regex": []},

    {"name": "Today Online", "url": "https://www.todayonline.com/news", "category": "sea", "enabled": False,
     "item_selector": "article", "title_selector": "a", "link_attr": "href", "date_selector": None, "date_attr": None,
     "summary_selector": None, "max_items": 30, "include_url_regex": [], "exclude_url_regex": []},

    # Thailand / Vietnam / etc. can be added in the same pattern...
]
