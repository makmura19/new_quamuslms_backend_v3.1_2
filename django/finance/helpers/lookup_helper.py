from helpers.custom_model_field import ObjectIdField, ObjectIdsField


def build_lookups(lookup_list, schema, foreign_key):
    pipeline = []

    for i in lookup_list:
        split = i.split(":")
        nested_field = []
        main_field = split[0]
        if len(split) == 2:
            nested_field = split[1].split(",")

        if main_field not in foreign_key:
            raise ValueError(f"Foreign key untuk '{main_field}' tidak ditemukan")

        fk = foreign_key[main_field]
        as_field = f"{fk['model'].collection_name}_info"

        pipeline.append(
            {
                "$lookup": {
                    "from": fk["model"].collection_name,
                    "localField": main_field,
                    "foreignField": fk["key"],
                    "as": as_field,
                }
            }
        )
        pipeline.append(
            {
                "$addFields": {
                    as_field: {
                        "$cond": {
                            "if": {"$eq": [f"${main_field}", None]},
                            "then": None,
                            "else": f"${as_field}",
                        }
                    }
                }
            }
        )

        field_type = schema._declared_fields.get(main_field)
        if isinstance(field_type, ObjectIdField):
            pipeline.append(
                {
                    "$unwind": {
                        "path": f"${as_field}",
                        "preserveNullAndEmptyArrays": True,
                    }
                }
            )

        pipeline.append(
            {
                "$project": {
                    f"{as_field}.is_deleted": 0,
                    f"{as_field}.created_at": 0,
                    f"{as_field}.updated_at": 0,
                }
            }
        )

        for j in nested_field:
            if j not in fk["model"].foreign_key:
                raise ValueError(
                    f"Nested foreign key '{j}' tidak ditemukan di model {fk['model'].__class__.__name__}"
                )
            nested_fk = fk["model"].foreign_key[j]
            nested_as = f"{nested_fk['model'].collection_name}_info"
            pipeline.append(
                {
                    "$lookup": {
                        "from": nested_fk["model"].collection_name,
                        "localField": f"{as_field}.{j}",
                        "foreignField": nested_fk["key"],
                        "as": nested_as,
                    }
                }
            )
            pipeline.append(
                {
                    "$project": {
                        f"{nested_as}.is_deleted": 0,
                        f"{nested_as}.created_at": 0,
                        f"{nested_as}.updated_at": 0,
                    }
                }
            )
    return pipeline
