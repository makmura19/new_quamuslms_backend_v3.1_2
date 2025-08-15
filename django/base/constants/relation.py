from enum import Enum


class RelationType(str, Enum):
    ONE_TO_ONE = "ONE_TO_ONE"
    ONE_TO_MANY = "ONE_TO_MANY"
    MANY_TO_MANY = "MANY_TO_MANY"
    MANY_TO_ONE = "MANY_TO_ONE"
