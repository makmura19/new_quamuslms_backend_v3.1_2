def handle_sum(value):
    if not isinstance(value, list):
        raise ValueError("SUM membutuhkan list.")
    return {"$sum": value}
