from urllib.parse import urlparse, urlunparse, parse_qsl, urlencode


TRACKING_PARAMS = {
    "utm_source",
    "utm_medium",
    "utm_campaign",
    "utm_term",
    "utm_content",
    "fbclid",
    "gclid",
    "mc_cid",
    "mc_eid",
    "ref",
    "ref_src",
    "igshid",
    "mkt_tok",
    "spm",
}


def canonicalize_url(raw_url: str) -> str:
    """
    Normalize and canonicalize URLs to improve deduplication.
    - force https where possible
    - remove tracking query params
    - sort remaining query params
    """
    if not raw_url:
        return raw_url

    try:
        parsed = urlparse(raw_url.strip())

        scheme = parsed.scheme or "https"
        netloc = (parsed.netloc or "").lower()
        path = (parsed.path or "").rstrip("/")

        # Filter query params
        query_params = [
            (k, v)
            for k, v in parse_qsl(parsed.query, keep_blank_values=True)
            if k.lower() not in TRACKING_PARAMS
        ]

        query = urlencode(sorted(query_params))

        return urlunparse((scheme, netloc, path, "", query, ""))
    except Exception:
        return raw_url
