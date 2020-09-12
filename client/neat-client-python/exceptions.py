from enum import Enum
from typing import List


class ErrorMessageEnum(Enum): 
    UNHANDLED_ERROR = '内部服务器错误:{}'
    UNEXPECTED_STATUS_CODE = "want status code {}, but got {}. response content: {}"


class NeatClientBaseException(Exception):
    MSG = ErrorMessageEnum.UNHANDLED_ERROR

    def __init__(self, params: List[str]):
        self.params = params
        message = self.MSG.value.format(*self.params)
        super().__init__(message)


class UnexpectedStatusCode(NeatClientBaseException):
    MSG = ErrorMessageEnum.UNEXPECTED_STATUS_CODE
