def handle_multiply(value):
    if not isinstance(value, list):
        raise ValueError("MULTIPLY membutuhkan list.")
    return {"$multiply": value}
