from typing import List
from mitmproxy.net.http.headers import Headers


def headers_to_list(headers: Headers) -> List[List]:
    result = []
    for i in headers.items():
        result.append([i[0], i[1]])
    return result


def list_to_headers(headers: List[List]) -> Headers:
    result = []
    for i in headers:
        result.append([i[0].encode("utf-8"), i[1].encode("utf-8")])
    return Headers(fields=result)
