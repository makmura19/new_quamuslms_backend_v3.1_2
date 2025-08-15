def handle_mask(value):
    """
    Membuat substr berdasarkan format masker seperti ###-##-##.
    value berupa: ["$medical_record_no", "###-##-##"]
    """
    if not isinstance(value, list) or len(value) != 2:
        raise ValueError("'value' harus berupa list dengan 2 elemen: [field, format]")

    field, pattern = value

    if not isinstance(field, str) or not isinstance(pattern, str):
        raise ValueError("'field' dan 'format' harus berupa string.")

    # Simpan nama field asli untuk digunakan dalam $cond
    original_field = field
    if field.startswith("$"):
        field = field[1:]

    substr_parts = []
    idx = 0
    digit_group = ""

    for char in pattern:
        if char == "#":
            digit_group += "#"
        else:
            if digit_group:
                length = len(digit_group)
                substr_parts.append({"$substr": [f"${field}", idx, length]})
                idx += length
                digit_group = ""
            substr_parts.append(char)

    if digit_group:
        length = len(digit_group)
        substr_parts.append({"$substr": [f"${field}", idx, length]})

    return {
        "$cond": {
            "if": {"$ne": [original_field, None]},
            "then": {"$concat": substr_parts},
            "else": None,
        }
    }
