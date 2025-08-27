from enum import Enum


class FieldType(str, Enum):
    DATE_TO_STRING = "DATE_TO_STRING"  # "value": "$birth.date"
    TIME = "TIME"  # "value": "$birth.date"
    DAY = "DAY"  # "value": "$birth.date"
    MONTH = "MONTH"  # "value": "$birth.date"
    YEAR = "YEAR"  # "value": "$birth.date"
    HOUR = "HOUR"  # "value": "$birth.date"
    MINUTE = "MINUTE"  # "value": "$birth.date"
    SECOND = "SECOND"  # "value": "$birth.date"
    DIFF_DAYS_FROM_TODAY = "DIFF_DAYS_FROM_TODAY"  # "value": "$birth.date"
    DAY_OF_WEEK = "DAY_OF_WEEK"  # "value": "$birth.date"
    DAY_OF_MONTH = "DAY_OF_MONTH"  # "value": "$birth.date"
    CONCAT = "CONCAT"  # "value": ["$address.street", " Ds. ", "$address.village"]

    SUM = "SUM"  # "value": ["$salary","$bonus"]
    SUBTRACT = "SUBTRACT"  # "value": ["$salary","$bonus"]
    MULTIPLY = "MULTIPLY"  # "value": ["$salary","$bonus"]
    MULTIPLY_WITH_CONSTANT = "MULTIPLY_WITH_CONSTANT"  # "value": ["$salary",2]
    DIVIDE = "DIVIDE"
    DIVIDE_WITH_CONSTANT = "DIVIDE_WITH_CONSTANT"
    ROUND = "ROUND"
    FORMAT_NUMBER = "FORMAT_NUMBER"

    STRING_LENGTH = "STRING_LENGTH"
    UPPERCASE = "UPPERCASE"
    LOWERCASE = "LOWERCASE"
    TRIM = "TRIM"
    LTRIM = "LTRIM"
    RTRIM = "RTRIM"
    REPLACE_STRING = "REPLACE_STRING"  # "value": ["$name","Hoe","Joe"]
    SPLIT_STRING = "SPLIT_STRING"  # "value": ["$name",","]

    ARRAY_LENGTH = "ARRAY_LENGTH"
    ELEMENT = "ELEMENT"  # "value": ["$array",0]
    ARRAY_SLICE = "ARRAY_SLICE"  # "value": ["$array",1,3]
    SUM_FROM_ARRAY_DICT = "SUM_FROM_ARRAY_DICT"
    AVG_FROM_ARRAY_DICT = "AVG_FROM_ARRAY_DICT"
    SUM_FROM_ARRAY = "SUM_FROM_ARRAY"
    AVG_FROM_ARRAY = "AVG_FROM_ARRAY"
    CONCAT_FROM_ARRAY_DICT = (
        "CONCAT_FROM_ARRAY_DICT"  # "value": ["$array_dic","field",","]
    )
    CONCAT_FROM_ARRAY = "CONCAT_FROM_ARRAY"
    ARRAY_FILTER = "ARRAY_FILTER"  # "value": ["$array_dict", {"is_active": True}]
    ARRAY_MERGE = "ARRAY_MERGE"
    ELEMENT_SPLIT = "ELEMENT_SPLIT"

    IF_NULL = "IF_NULL"
    EXISTS = "EXISTS"

    CAST_INT = "CAST_INT"
    CAST_STRING = "CAST_STRING"
    CAST_NUMBER = "CAST_NUMBER"

    RENAME_FIELD = "RENAME_FIELD"
    SWITCH = "SWITCH"
    AGE = "AGE"
    HANDLE_MASK = "HANDLE_MASK"


class GroupAggregationOp(str, Enum):
    GROUP_AVG = "avg"
    GROUP_SUM = "sum"
    GROUP_MAX = "max"
    GROUP_MIN = "min"


class UpdateOperator(str, Enum):
    SET = "$set"
    INC = "$inc"  # {"$inc": {"balance": 100}}
    DEC = "$inc"
    ADD_TO_SET = "$addToSet"  # {"$addToSet": {"skills": {"$each": ["Python", "JavaScript", "Go"]}}}
    PULL_ALL = "$pullAll"  # {"$pullAll": {"skills": ["Python", "Java"]}}
    CURRENT_DATE = "$currentDate"
