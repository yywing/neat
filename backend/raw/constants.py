from enum import Enum


class SchemeEnum(Enum):
    HTTP = 'http'
    HTTPS = "https"


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
