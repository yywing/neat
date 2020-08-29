
'''
use mitmproxy http request and response type
'''
import pathlib
from io import BytesIO
from urllib.parse import urlparse, urlunparse

from mitmproxy.net.http.request import Request as _Request
from mitmproxy.net.http.response import Response
from mitmproxy.net.http.http1 import read


class Request(_Request):
    @classmethod
    def from_origin_class(cls, r: _Request):
        # It works.
        r.__class__ = cls
        return r

    @property
    def suffix(self):
        return pathlib.Path(self.pure_url).suffix[1:]

    @property
    def pure_url(self):
        return get_pure_url(self.url)


def parse_request(scheme, host, port, raw_request) -> Request:
    raw = BytesIO(raw_request)
    request = read.read_request(raw)
    request.scheme = scheme
    request.port = port
    request.host = host
    return Request.from_origin_class(request)


def parse_response(raw_response, request: Request) -> Response:
    raw = BytesIO(raw_response)
    response = read.read_response(raw, request)
    return response


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
