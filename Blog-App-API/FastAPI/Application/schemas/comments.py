from pydantic import BaseModel, Field
from typing import Optional
from bson import ObjectId
from datetime import datetime


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class CommentBase(BaseModel):
    text: str = Field(..., min_length=1, max_length=500)
    blog_id: str = Field(..., alias="blog_id", description="ID of the associated blog post.")
    author: str = Field(..., min_length=3, max_length=100, description="Name of the comment author.")

class CommentCreate(CommentBase):
    pass

class CommentUpdate(BaseModel):
    text: Optional[str] = Field(None, min_length=1, max_length=500)

class CommentResponse(CommentBase):
    id: str = Field(..., alias="_id")
    created_at: datetime

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class OneComment(BaseModel):
    id: str
    text: str
    author: str
    blog_id: str
    creation: datetime


class CommentsList(BaseModel):
    comments: list[OneComment]
    total: int