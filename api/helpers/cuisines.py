from utils.models import Cuisines
from bson import ObjectId

def serialize_document(cuisine=Cuisines):
    """
    Converts MongoDB ObjectId and other types to JSON-serializable formats.
    """
    cuisine["_id"] = int(cuisine["_id"])
    return cuisine

def query_builder(id=None,name=None):
    """
    Builds a query for MongoDB based on the provided parameters.
    """
    args = {}
    if id is not None:
        if isinstance(id, list) and len(id) > 1:
            args['_id'] = {"$in": [int(i) for i in id]}
        elif isinstance(id, list) and len(id) == 1:
            args['_id'] = int(id[0])
        else:
            args['_id'] = int(id)
    if name is not None:
        if isinstance(name, list) and len(name) > 1:
            args['name'] = {"$in": [name for name in name]}
        elif isinstance(name, list) and len(name) == 1:
            args['name'] = name[0]
        else:
            args['name'] = name
    return args

