from urllib.parse import urlparse, urlunparse


def get_root_website(url) -> str:
    url = urlparse(url)
    netloc = url.netloc.lower()
    port = url.port
    scheme = url.scheme
    default_port_number = {80: 'http', 443: 'https'}
    if default_port_number.get(port) == scheme:
        netloc = url.hostname.lower()
    url = urlunparse((scheme, netloc, '/', '', '', ''))
    return url


def get_pure_url(url) -> str:
    url = urlparse(url)
    netloc = url.netloc.lower()
    scheme = url.scheme
    port = url.port
    # XRAY-4070
    path = url.path if url.path != '' else '/'

    default_port_number = {80: 'http', 443: 'https'}
    if default_port_number.get(port) == scheme:
        netloc = url.hostname.lower()
    url = urlunparse((scheme, netloc, path, "", "", ""))
    return url


def get_query_string(url) -> str:
    url = urlparse(url)
    return url.query
