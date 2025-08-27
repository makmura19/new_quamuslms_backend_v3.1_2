from datetime import datetime, timezone
from constants.aggregation import FieldType


def build_add_fields(definitions: dict):
    result = {}
    today = datetime.now(timezone.utc).astimezone().date()
    today_datetime = datetime(today.year, today.month, today.day, tzinfo=timezone.utc)

    for key, field in definitions.items():
        val = field["value"]
        if field["type"] == FieldType.CONCAT:
            result[key] = {"$concat": val}
        elif field["type"] == FieldType.DATE_TO_STRING:
            result[key] = {"$dateToString": {"format": "%d-%m-%Y", "date": val}}
        elif field["type"] == FieldType.TIME:
            result[key] = {"$dateToString": {"format": "%H:%M:%S", "date": val}}
        elif field["type"] == FieldType.DAY:
            result[key] = {"$dayOfMonth": val}
        elif field["type"] == FieldType.MONTH:
            result[key] = {"$month": val}
        elif field["type"] == FieldType.YEAR:
            result[key] = {"$year": val}
        elif field["type"] == FieldType.HOUR:
            result[key] = {"$hour": val}
        elif field["type"] == FieldType.MINUTE:
            result[key] = {"$minute": val}
        elif field["type"] == FieldType.SECOND:
            result[key] = {"$second": val}
        elif field["type"] == FieldType.DIFF_DAYS_FROM_TODAY:
            result[key] = {
                "$toInt": {
                    "$divide": [
                        {
                            "$subtract": [
                                today_datetime,
                                {
                                    "$dateFromString": {
                                        "dateString": {
                                            "$dateToString": {
                                                "format": "%Y-%m-%d",
                                                "date": val,
                                            }
                                        }
                                    }
                                },
                            ]
                        },
                        86400000,
                    ]
                }
            }
        elif field["type"] == FieldType.DAY_OF_WEEK:
            result[key] = {"$dayOfWeek": val}
        elif field["type"] == FieldType.DAY_OF_MONTH:
            result[key] = {
                "$toInt": {
                    "$ceil": {
                        "$divide": [
                            {"$subtract": [{"$dayOfMonth": val}, 1]},
                            7,
                        ]
                    }
                }
            }
    return result
