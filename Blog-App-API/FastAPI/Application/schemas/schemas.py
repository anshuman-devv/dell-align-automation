# def OneNote(item):
#     return {
#         "id": str(item["_id"]),
#         "title": item["title"],
#         "content": item["content"]
#     }


# def NotesList(items):
#     return [OneNote(item) for item in items]
    

# def OneComment(item):
#     return {
#         "id": str(item["_id"]),
#         "text": item["text"],
#         "author": item["author"],
#         "blog_id": item["blog_id"],
#         "creation": item["creation"]
#     }

# def CommentsList(items):
#     return [OneComment(item) for item in items]




from pydantic import BaseModel, Field, root_validator
from typing import Optional, List
from datetime import datetime
from bson import ObjectId
from Application.schemas.comments import CommentsList



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



class BlogBase(BaseModel):
    title: str = Field(..., min_length=3, max_length=100)
    content: str
    author: str

class BlogCreate(BlogBase):
    pass

class BlogUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=3, max_length=100)
    content: Optional[str]

class BlogResponse(BaseModel):
    id: str
    title: str
    content: str
    created_at: datetime
    # comments = List[CommentsList]

    @root_validator(pre=True)
    def convert_objectid(cls, values):
        if '_id' in values:
            values['id'] = str(values['_id'])  
            del values['_id'] 
        return values
