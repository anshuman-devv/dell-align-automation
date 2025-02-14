from datetime import datetime
from bson import ObjectId


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


class CommentModel:
    def __init__(self, text: str, blog_id: str, author: str):
        self.text = text
        self.blog_id = ObjectId(blog_id)  
        self.author = author  
        self.created_at = datetime.utcnow()
