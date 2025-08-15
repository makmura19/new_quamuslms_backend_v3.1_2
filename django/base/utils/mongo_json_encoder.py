import json
from bson import ObjectId
from datetime import datetime


class MongoJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        if isinstance(o, datetime):
            return o.isoformat() + "Z"
        return super().default(o)
