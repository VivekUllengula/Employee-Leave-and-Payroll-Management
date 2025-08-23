from bson import ObjectId
from pydantic import BaseModel, Field

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if isinstance(v, ObjectId):
            return v
        if isinstance(v, str) and ObjectId.is_valid(v):
            return ObjectId(v)
        raise ValueError("Invalid ObjectId")
    
class DBModelMixin(BaseModel):
    id: PyObjectId | None = Field(default=None, alias="_id")

    class Config:
        populate_ny_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

