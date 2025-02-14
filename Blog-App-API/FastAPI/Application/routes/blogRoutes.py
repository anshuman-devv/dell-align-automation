from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from Application.schemas.schemas import *
from Application.schemas.comments import *
from Application.config.db import coll, comments_coll
from Application.routes.userRoutes import check_author
from Application.routes.auth import get_current_user


blog_router = APIRouter()


@blog_router.get('/')
async def readBlogs(page: int = 1, page_size: int = 2):
    try:
        print("Reading blogs")
        blogs = coll.find().skip((page - 1) * page_size).limit(page_size)
        blog_list = blogs.to_list(length=page_size)
        return {
            "blogs": [
                BlogResponse(**{**blog, "id": str(blog["_id"]),
                                 "created_at": datetime.fromtimestamp(blog["creation"]),
                                 "comments": blog.get("comments", [])})
                for blog in blog_list
            ],
            "total": coll.count_documents({})
        }
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="An error occurred while fetching blogs")


@blog_router.get('/{blog_id}')
async def readOneBlog(blog_id: str):
    try:
        id = ObjectId(blog_id)
        blog = coll.find_one({"_id": id})
        if not blog:
            raise HTTPException(status_code=404, detail="Blog not found")
        
        comments = comments_coll.find({"blog_id": blog_id})
        comment_list = comments.to_list(length=5)
        
        return {
            "blog": BlogResponse(**blog, created_at=datetime.fromtimestamp(blog["creation"])),
            "comments": [CommentResponse(**comment, creation=datetime.fromtimestamp(comment["creation"])) for comment in comment_list]
        }
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="An error occurred while fetching blog details")


@blog_router.post('/create')
async def createBlog(request: BlogCreate, current_user: str = Depends(get_current_user)):
    try:
        blog_data = request.model_dump()
        blog_data['author'] = current_user
        blog_data['creation'] = int(datetime.timestamp(datetime.now()))
        coll.insert_one(blog_data)
        return JSONResponse(status_code=201, content={"message": "Blog created successfully"})
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to create blog")

@blog_router.put('/{blog_id}/update')
async def updateBlog(blog_id: str, updated_blog: BlogUpdate, current_user: str = Depends(get_current_user)):
    check_author(blog_id, current_user)
    print("User valid")
    try:
        result = coll.update_one({"_id": ObjectId(blog_id)}, {"$set": updated_blog.model_dump()})
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Blog not found")
        return {"message": "Blog updated successfully"}
    
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Failed to update blog")

@blog_router.delete('/{blog_id}/delete')
async def deleteBlog(blog_id: str, current_user: str = Depends(get_current_user)):
    check_author(blog_id, current_user)
    try:
        result = coll.update_one({"_id": ObjectId(blog_id)}, {"$set": {"is_deleted": True}})
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Blog not found")
        
        comments_coll.update_many({"blog_id": blog_id}, {"$set": {"is_deleted": True}})
        return {"message": "Blog and associated comments deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to delete blog")
