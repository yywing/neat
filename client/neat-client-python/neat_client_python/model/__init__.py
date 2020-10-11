from enum import Enum
import json
from urllib.parse import urljoin

from requests import Request, Response
from ..exceptions import UnexpectedStatusCode


API_PREFIX = "/api/"


class HTTPMethod(Enum):
    GET = "GET"
    POST = "POST"


class HTTPSchema(Enum):
    HTTP = "http"
    HTTPS = "https"


class BaseModel:
    auth = True

    def to_request(self, base_url, headers):
        url = urljoin(base_url, self.uri)
        data = json.dumps(self.request_data._asdict())
        req = Request(self.method, url, data=data, headers=headers)
        return req

    def from_response(self, response: Response):
        if response.status_code != self.status_code:
            raise UnexpectedStatusCode(
                params=[self.status_code, response.status_code, response.content])
        data = response.json()
        return self.response_class(**data)
