from enum import Enum


class Module(str, Enum):
    LMS = "lms"
    ATTENDANCE = "attendance"
    FINANCE = "finance"
    TAHFIDZ = "tahfidz"
    TAHSIN = "tahsin"
    PRA_TAHSIN = "pra_tahsin"
    MUTABAAH = "mutabaah"
    ARABIC = "arabic"
    MEDIA = "media"
