def handle_rename_field(value):
    if not isinstance(value, list) or len(value) != 1:
        raise ValueError("RENAME_FIELD membutuhkan list berisi 1 item (nama lama).")
    old_field = value[0]
    return f"${old_field}", old_field  # result, field to be removed
