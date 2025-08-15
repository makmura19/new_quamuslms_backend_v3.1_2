import json
import os


class JsonUtil:
    @staticmethod
    def smart_json_loads(s):
        try:
            data = json.loads(s)
            if isinstance(data, str):
                return json.loads(data)
            return data
        except Exception:
            return {}

    @staticmethod
    def read(filepath):
        try:
            if not os.path.exists(filepath):
                return {}

            with open(filepath, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}

    @staticmethod
    def write(filepath, data, indent=4):
        try:
            os.makedirs(os.path.dirname(filepath), exist_ok=True)

            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=indent, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Failed to write JSON to file: {e}")
            return False
