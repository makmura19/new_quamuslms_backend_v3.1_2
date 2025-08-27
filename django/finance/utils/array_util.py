from bson import ObjectId


class ArrayUtil:
    @staticmethod
    def has_intersection(list1, list2):
        for item in list1:
            if item in list2:
                return True
        return False

    @staticmethod
    def add_sequence(data: list):
        for i, item in enumerate(data, start=1):
            item["sequence"] = i
            for key, value in item.items():
                if isinstance(value, list) and all(isinstance(v, dict) for v in value):
                    ArrayUtil.add_sequence(value)
        return data

    @staticmethod
    def is_unique(data_list, key=None):
        seen = set()
        for item in data_list:
            if key is None:
                val = item
            elif isinstance(key, list):
                val = tuple(item.get(k) for k in key)
            else:
                val = item.get(key)

            if val in seen:
                return False
            seen.add(val)
        return True

    @staticmethod
    def isWhitelistedUniqueItems(ref, test):
        if len(test) != len(set(test)):
            return False
        if not set(test).issubset(set(ref)):
            return False
        return True

    @staticmethod
    def replace_new_ids(obj, isObjectId=True):
        if isinstance(obj, dict):
            new_obj = {}
            for k, v in obj.items():
                new_obj["is_new"] = False
                if k == "_id":
                    if isinstance(v, str) and v.startswith("new_"):
                        new_obj["is_new"] = True
                        new_obj[k] = ObjectId() if isObjectId else str(ObjectId())
                    elif isObjectId and not isinstance(v, ObjectId):
                        try:
                            new_obj[k] = ObjectId(v)
                        except Exception:
                            new_obj[k] = v
                    else:
                        new_obj[k] = v
                else:
                    new_obj[k] = ArrayUtil.replace_new_ids(v, isObjectId)
            return new_obj
        elif isinstance(obj, list):
            return [ArrayUtil.replace_new_ids(i, isObjectId) for i in obj]
        else:
            return obj
