from enum import Enum
from io import BytesIO
import re

from mitmproxy.net.http.response import Response as _Response
from mitmproxy.net.http.http1 import read

from .request import Request
from .mime import (
    check_json, check_form, check_other, check_html,
    check_xml, check_image, check_empty, check_font,
    check_js, check_css
)

JSONP_RE = jsonp_re = re.compile(r"^([a-zA-Z][a-zA-z$_]?.)+\(*\)$")


class ResponseTypeEnum(Enum):
    # no content type
    empty = "empty"

    jsonp = "jsonp"

    html = "html"

    json = "json"
    form = "form"
    xml = "xml"

    # file
    image = "image"
    font = "font"
    css = "css"
    js = "js"

    other = "other"

    @classmethod
    def check_empty(cls, content_type, content) -> bool:
        return check_empty(content_type, content)

    @classmethod
    def check_jsonp(cls, content_type, content) -> bool:
        # TODO: content 编码问题
        return True if JSONP_RE.match(content) else False

    @classmethod
    def check_html(cls, content_type, content) -> bool:
        return check_html(content_type, content)

    @classmethod
    def check_json(cls, content_type, content) -> bool:
        return check_json(content_type, content)

    @classmethod
    def check_form(cls, content_type, content) -> bool:
        return check_form(content_type, content)

    @classmethod
    def check_xml(cls, content_type, content) -> bool:
        return check_xml(content_type, content)

    @classmethod
    def check_image(cls, content_type, content) -> bool:
        return check_image(content_type, content)

    @classmethod
    def check_font(cls, content_type, content) -> bool:
        return check_font(content_type, content)

    @classmethod
    def check_css(cls, content_type, content) -> bool:
        return check_css(content_type, content)

    @classmethod
    def check_js(cls, content_type, content) -> bool:
        return check_js(content_type, content)

    @classmethod
    def check_other(cls, content_type, content) -> bool:
        return check_other(content_type, content)

    @classmethod
    def get_response_type(cls, content_type, content):
        for enum_item in cls:
            result = getattr(cls, f"check_{enum_item.name}")
            if result:
                return enum_item
        return cls.other


class Response(_Response):
    @classmethod
    def from_origin_class(cls, r: _Response):
        # It works.
        r.__class__ = cls
        return r

    @property
    def content_type(self):
        return self.headers.get("content-type", "").lower()

    @property
    def response_type(self) -> str:
        return ResponseTypeEnum.get_response_type(self.content_type, self.content).value


def parse_response(raw_response, request: Request) -> Response:
    raw = BytesIO(raw_response)
    response = read.read_response(raw, request)
    return Response.from_origin_class(response)
