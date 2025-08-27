def handle_age(value):
    return {
        "$dateDiff": {
            "startDate": value,
            "endDate": "$$NOW",
            "unit": "year",
        }
    }
