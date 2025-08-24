from bson import ObjectId
from datetime import date, datetime
 
def normalize_document(doc: dict) -> dict:
    """Convert date to datetime for MongoDB compatibility"""
    for key, value in doc.items():
        if isinstance(value, date) and not isinstance(value, datetime):
            # Convert date → datetime at midnight
            doc[key] = datetime(value.year, value.month, value.day)
    return doc
 
def convert_mongo_document(doc: dict) -> dict:
    """
    Convert MongoDB document (with ObjectId) into JSON-serializable dict.
    """
    if not doc or not isinstance(doc, dict):
        return None
    doc = dict(doc)
    if "_id" in doc and isinstance(doc["_id"], ObjectId):
        doc["_id"] = str(doc["_id"])
    return doc
 
def convert_many(docs: list) -> list:
    if not docs:
        return []
    return [convert_mongo_document(doc) for doc in docs if doc]