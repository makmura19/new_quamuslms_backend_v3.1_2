from enum import Enum


class NotificationCode(str, Enum):
    PATIENT_APPROVAL = "n01"
    DONOR_APPROVAL = "n02"
