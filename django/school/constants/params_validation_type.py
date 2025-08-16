from enum import Enum


class ParamsValidationType(str, Enum):
    DATE = "DATE"
    DATETIME = "DATETIME"
    DATETIME_TO_UTC = "DATETIME_TO_UTC"
    INT = "INT"
    BOOLEAN = "BOOLEAN"
    STRING = "STRING"
    LIST_STRING = "LIST_STRING"
    OBJECT_ID = "OBJECT_ID"
    OBJECT_IDS = "OBJECT_IDS"
    UNKNOWN = "UNKNOWN"
