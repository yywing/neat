from typing import NamedTuple, Optional
from http import HTTPStatus
from os.path import join

from . import BaseModel, HTTPMethod, API_PREFIX


class GetTokenRequest(NamedTuple):
    username: str
    password: str


class TokenRespose(NamedTuple):
    token: str


class Token(BaseModel):
    uri = join(API_PREFIX, "token/")
    auth = False
    method = HTTPMethod.POST.value
    status_code = HTTPStatus.OK
    request_class = GetTokenRequest
    response_class = TokenRespose

    def __init__(self, request_data):
        self.request_data = request_data


class VerifyTokenRequest(NamedTuple):
    token: str


class VerifyToken(BaseModel):
    uri = join(API_PREFIX, "token/verify")
    auth = False
    method = HTTPMethod.POST.value
    status_code = HTTPStatus.OK
    request_class = VerifyTokenRequest
    response_class = TokenRespose

    def __init__(self, request_data):
        self.request_data = request_data
