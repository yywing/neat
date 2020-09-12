from typing import NamedTuple
from http import HTTPStatus
from os.path import join

from . import BaseModel, HTTPMethod, API_PREFIX


class CreateRawRequest(NamedTuple):
    raw_request: str
    raw_response: str
    scheme: str
    host: str
    port: int


class RawRespose(NamedTuple):
    id: int
    url: int
    raw_request: str
    raw_response: str
    scheme: str
    host: str
    port: int
    created_time: str


class CreateRaw(BaseModel):
    uri = join(API_PREFIX, "raw/")
    method = HTTPMethod.POST.value
    status_code = HTTPStatus.CREATED
    request_class = CreateRawRequest
    response_class = RawRespose

    def __init__(self, request_data):
        self.request_data = request_data
