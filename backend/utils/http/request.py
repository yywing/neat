from enum import Enum
from io import BytesIO
import pathlib

from mitmproxy.net.http.request import Request as _Request
from mitmproxy.net.http.http1 import read

from .mime import check_json, check_form, check_other, check_empty
from .utils import get_pure_url


class RequestTypeEnum(Enum):
    # no content type
    empty = "empty"

    json = "json"
    form = "form"
    other = "other"

    @classmethod
    def check_empty(cls, content_type, content) -> bool:
        return check_empty(content_type, content)

    @classmethod
    def check_json(cls, content_type, content) -> bool:
        return check_json(content_type, content)

    @classmethod
    def check_form(cls, content_type, content) -> bool:
        return check_form(content_type, content)

    @classmethod
    def check_other(cls, content_type, content) -> bool:
        return check_other(content_type, content)

    @classmethod
    def get_request_type(cls, content_type, content):
        for enum_item in cls:
            result = getattr(cls, f"check_{format(enum_item.name)}")
            if result:
                return enum_item
        return cls.other


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

    @property
    def content_type(self):
        return self.headers.get("content-type", "").lower()

    @property
    def request_type(self) -> str:
        return RequestTypeEnum.get_request_type(self.content_type, self.content).value


def parse_request(scheme, host, port, raw_request) -> Request:
    raw = BytesIO(raw_request)
    request = read.read_request(raw)
    request.scheme = scheme
    request.port = port
    request.host = host
    return Request.from_origin_class(request)
