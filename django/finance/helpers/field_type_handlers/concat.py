def handle_concat(value):
    if not isinstance(value, list):
        raise ValueError("CONCAT membutuhkan list sebagai value.")
    return {"$concat": value}
