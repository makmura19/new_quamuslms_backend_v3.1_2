def handle_round(value):
    if not isinstance(value, list) or len(value) != 2:
        raise ValueError("ROUND membutuhkan 2 parameter: [field, precision]")
    return {"$round": value}
