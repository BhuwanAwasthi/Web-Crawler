# crawler/utils.py

from urllib.parse import urlparse, urlunparse

def normalize_url(url):
    parsed = urlparse(url)
    scheme = parsed.scheme or 'http'
    netloc = parsed.netloc
    path = parsed.path
    normalized_url = urlunparse((scheme, netloc, path, '', '', ''))
    return normalized_url.rstrip('/')

def is_allowed_domain(url, allowed_domains):
    netloc = urlparse(url).netloc
    return any(netloc.endswith(domain) for domain in allowed_domains)
