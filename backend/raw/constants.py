from enum import Enum


class SchemaEnum(Enum):
    HTTP = 'http://'
    HTTPS = "https://"


class RequestMethodEnum(Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    PATCH = "PATCH"
    DELETE = "DELETE"
    MOVE = "MOVE"
    COPY = "COPY"

    HEAD = "HEAD"
    OPTIONS = "OPTIONS"
    TRACE = "TRACE"
    LINK = "LINK"
    UNLINK = "UNLINK"
    WRAPPED = "WRAPPED"
    EXTENSION_METHOD = "EXTENSION_METHOD"


class RequestTypeEnum(Enum):
    NOEMAL = "normal"
    GRAPHQL = "graphql"


class ResponseTypeEnum(Enum):
    HTML = "html"
    PlAIN = "plain"
    CSS = "css"
    JS = "js"
    FONT = "font"
    IMG = "img"
    JSON = "json"
    JSONP = "jsonp"
