from bson import ObjectId
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from pydantic_core import core_schema
from pydantic.json_schema import JsonSchemaValue
from pydantic import GetCoreSchemaHandler, GetJsonSchemaHandler
 
 
class PyObjectId(ObjectId):
    """
    Custom Pydantic-compatible ObjectId field for MongoDB.
    Works with Pydantic v2 validation and JSON schema generation.
    """
 
    @classmethod
    def __get_pydantic_core_schema__(cls, _source_type, _handler: GetCoreSchemaHandler):
        return core_schema.no_info_after_validator_function(
            cls.validate,
            core_schema.str_schema()
        )
 
    @classmethod
    def validate(cls, value):
        if not ObjectId.is_valid(value):
            raise ValueError("Invalid ObjectId")
        return ObjectId(value)
 
    @classmethod
    def __get_pydantic_json_schema__(cls, _core_schema, handler: GetJsonSchemaHandler) -> JsonSchemaValue:
        # Tells OpenAPI/Swagger that this field is a string
        return {"type": "string", "example": "64c9f4f2d1b8f9a7e9d12345"}
 
 
class DBModelMixin(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
 
    class Config:
        json_encoders = {
            ObjectId: str,
            datetime: lambda v: v.isoformat(),
        }
        populate_by_name = True