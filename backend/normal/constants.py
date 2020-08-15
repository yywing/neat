from enum import Enum


class ValueTypeEnum(Enum):
    String = "string"
    Integer = "integer"
    Boolean = "boolean"
    Object = "object"
    Unknown = "unknown"


class ParamPositionEnum(Enum):
    QUERY = "query"
    BODY = "body"


class ParamTypeEnum(Enum):
    JSON = "json"
    UNKNOWN = "unknown"
