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
    Convert MongoDB document to JSON-serializable dict.
    - ObjectId -> str
    - datetime/date -> ISO string
    """
    if not doc:
        return None
 
    new_doc = {}
    for key, value in doc.items():
        if isinstance(value, ObjectId):
            new_doc[key] = str(value)
        elif isinstance(value, (datetime, date)):
            new_doc[key] = value.isoformat()
        elif isinstance(value, dict):  # nested docs
            new_doc[key] = convert_mongo_document(value)
        elif isinstance(value, list):  # list of docs
            new_doc[key] = [convert_mongo_document(v) if isinstance(v, dict) else str(v) if isinstance(v, ObjectId) else v for v in value]
        else:
            new_doc[key] = value
    return new_doc
 
def convert_many(docs: list) -> list:
    if not docs:
        return []
    return [convert_mongo_document(doc) for doc in docs if doc]