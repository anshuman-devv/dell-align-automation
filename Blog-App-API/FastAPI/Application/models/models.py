from pydantic import BaseModel, Field
from datetime import datetime


class Blog(BaseModel):
    title: str = Field(..., min_length=1, max_length=100, description="Title of the blog")
    content: str = Field(..., min_length=1, description="Content of the blog")
    author: str = Field(..., min_length=1, description="Author of the blog")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Creation timestamp of the blog")


class Comment(BaseModel):
    text: str = Field(..., min_length=1, description="Comment text")
    author: str = Field(..., min_length=1, description="Author of the comment")
    blog_id: str = Field(..., description="ID of the blog post this comment is associated with")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Creation timestamp of the comment")



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


class BlogModel:
    def __init__(self, title: str, content: str, author: str):
        self.title = title
        self.content = content
        self.author = author
        self.created_at = datetime.utcnow()


class BlogWithComments(BlogModel):
    def __init__(self, blog_data, comments_data):
        super().__init__(title=blog_data["title"], content=blog_data["content"], author=blog_data["author"])
        self.comments = comments_data

        