from datetime import datetime, timedelta
from bson import ObjectId
from constants.params_validation_type import ParamsValidationType
from datetime import datetime
from pytz import timezone, UTC


def build_find_query(query_params, params_validation, tz_str="UTC"):
    """
    Membuat query MongoDB dari parameter GET berbasis validasi tipe data.

    Fitur:
    ------
    - Mendukung operator: __eq (default), __ne, __gt, __gte, __lt, __lte, __in
    - Mendukung operator tanggal spesifik: __year, __month (menghasilkan `$expr`)
    - Mendukung operator ukuran array: __size__gt, __size__eq, dll (menghasilkan `$expr`)
    - Mendukung konversi otomatis ke:
      - int (ParamsValidationType.INT)
      - bool (ParamsValidationType.BOOLEAN)
      - datetime/date ke UTC (ParamsValidationType.DATETIME, ParamsValidationType.DATE, ParamsValidationType.DATETIME_TO_UTC)
      - ObjectId (ParamsValidationType.OBJECT_ID)
      - string (ParamsValidationType.STRING)

    Khusus ParamsValidationType.DATE:
    ---------------------------------
    - Jika menggunakan operator __gt/__gte: waktu otomatis menjadi 00:00:00 (awal hari)
    - Jika menggunakan operator __lt/__lte: waktu otomatis menjadi 23:59:59 (akhir hari)

    Parameters:
    -----------
    query_params : dict
        Parameter dari request query string.
        Contoh:
        {
            "age__gte": "25",
            "birthdate__year": "1990",
            "class_ids__size__gt": "0"
        }

    params_validation : dict
        Validasi mapping field dengan tipe datanya.
        Contoh:
        {
            "age": ParamsValidationType.INT,
            "birthdate": ParamsValidationType.DATE,
            "class_ids": ParamsValidationType.STRING
        }

    Returns:
    --------
    dict
        Query MongoDB yang sudah terformat sesuai validasi.

    Contoh Output:
    --------------
    {
        "age": { "$gte": 25 },
        "$expr": {
            "$eq": [ { "$year": "$birthdate" }, 1990 ]
        }
    }

    """
    from datetime import datetime, timedelta
    from pytz import timezone, UTC
    from bson import ObjectId

    query = {}
    query_arr = {}

    for key, value in query_params.items():
        if key in ["page", "size", "sort", "search"]:
            continue

        key_split = key.split("__")
        operator = "$eq"
        fields = key
        spesific = None
        use_size = False

        # Detect operator
        if len(key_split) > 2 and key_split[-2] == "size":
            use_size = True
            operator = f"${key_split[-1]}"
            fields = "__".join(key_split[0:-2])
        elif len(key_split) > 1:
            if key_split[-1] in ["ne", "gt", "gte", "lt", "lte", "in"]:
                operator = f"${key_split[-1]}"
                fields = "__".join(key_split[0:-1])
            elif key_split[-1] in ["month", "year"]:
                spesific = f"${key_split[-1]}"
                fields = "__".join(key_split[0:-1])

        if fields not in params_validation:
            continue

        type_ = params_validation[fields]
        fields = fields.replace("__", ".")
        if fields not in query_arr:
            query_arr[fields] = []

        if use_size:
            value = int(value)
            query_arr[fields].append(
                {"operator": operator, "value": value, "spesific": "$size"}
            )
            continue

        # Handle type conversion
        if type_ == ParamsValidationType.INT:
            value = None if value == "null" else int(value)
        elif type_ == ParamsValidationType.BOOLEAN:
            value = value == "true"
        elif type_ == ParamsValidationType.DATETIME_TO_UTC:
            dt_str = f"{value} 00:00:00"
            local_tz = timezone(tz_str)
            local_dt = datetime.strptime(dt_str, "%Y-%m-%d %H:%M:%S")
            local_dt = local_tz.localize(local_dt)
            local_dt = local_dt.astimezone(UTC)
            value = local_dt
        elif type_ == ParamsValidationType.DATE:
            local_tz = timezone(tz_str)
            if operator in ["$gte", "$gt"]:
                dt = datetime.strptime(value, "%Y-%m-%d")
            elif operator in ["$lte", "$lt"]:
                dt = datetime.strptime(value, "%Y-%m-%d") + timedelta(
                    hours=23, minutes=59, seconds=59
                )
            else:
                dt = datetime.strptime(value, "%Y-%m-%d")
            local_dt = local_tz.localize(dt)
            local_dt = local_dt.astimezone(UTC)
            value = local_dt
        elif type_ == ParamsValidationType.DATETIME:
            value = datetime.strptime(value, "%Y-%m-%d")
        elif type_ == ParamsValidationType.OBJECT_ID:
            value = None if value == "null" else ObjectId(value)
        elif type_ == ParamsValidationType.STRING:
            value = None if value == "null" else value

        # Spesial perlakuan untuk DATETIME_TO_UTC dengan operator eq
        if (
            operator == "$eq"
            and type_ == ParamsValidationType.DATETIME_TO_UTC
            and spesific is None
        ):
            query_arr[fields].append(
                {"operator": "$gte", "value": value, "spesific": spesific}
            )
            query_arr[fields].append(
                {
                    "operator": "$lt",
                    "value": value + timedelta(hours=24),
                    "spesific": spesific,
                }
            )
        elif operator == "$in":
            query_arr[fields].append(
                {"operator": operator, "value": value.split(","), "spesific": spesific}
            )
        else:
            query_arr[fields].append(
                {"operator": operator, "value": value, "spesific": spesific}
            )

    for k, v in query_arr.items():
        if v[0]["spesific"] is None:
            query[k] = {i["operator"]: i["value"] for i in v}
        else:
            expr = []
            for i in v:
                field_expr = (
                    {"$size": f"${k}"}
                    if i["spesific"] == "$size"
                    else {i["spesific"]: f"${k}"}
                )
                expr.append({i["operator"]: [field_expr, i["value"]]})
            query["$expr"] = expr[0] if len(expr) == 1 else {"$and": expr}

    return query
