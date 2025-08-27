def handle_date_to_string(value):
    return {"$dateToString": {"format": "%d-%m-%Y", "date": value}}
