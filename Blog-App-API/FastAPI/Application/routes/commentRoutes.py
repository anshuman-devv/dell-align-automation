from fastapi import Depends, HTTPException, APIRouter
from Application.config.db import comments_coll
from Application.schemas.comments import OneComment, CommentsList, CommentCreate, CommentUpdate, CommentResponse
from datetime import datetime
from bson.objectid import ObjectId
from Application.routes.auth import get_current_user
from fastapi.responses import JSONResponse

comment_router = APIRouter()


@comment_router.post('/blog/{blog_id}/create')
async def createComment(blog_id: str, comment: CommentCreate, current_user: str = Depends(get_current_user)):
    try:
        comment_data = comment.model_dump()
        comment_data['blog_id'] = blog_id
        comment_data['author'] = current_user
        comment_data['creation'] = int(datetime.timestamp(datetime.now()))
        comments_coll.insert_one(comment_data)
        return JSONResponse(status_code=201, content={"message": "Comment added successfully"})
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to add comment")

@comment_router.get('/{comment_id}')
async def readComment(comment_id: str):
    try:
        comment = comments_coll.find_one({"_id": ObjectId(comment_id)})
        if not comment:
            raise HTTPException(status_code=404, detail="Comment not found")
        comment['id'] = str(comment.pop('_id'))
        return OneComment(**comment)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=404, detail="Failed to fetch comment")


@comment_router.put('/{comment_id}/update')
async def updateComment(comment_id: str, updated_comment: CommentUpdate, current_user: str = Depends(get_current_user)):
    try:
        comment = comments_coll.find_one({"_id": ObjectId(comment_id)})
        if not comment:
            raise HTTPException(status_code=404, detail="Comment not found")
        
        if comment["author"] != current_user:
            raise HTTPException(status_code=403, detail="Not authorized to update this comment")
        
        updated_data = updated_comment.dict(exclude_unset=True)
        comments_coll.update_one({"_id": ObjectId(comment_id)}, {"$set": updated_data})
        return {"message": "Comment updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to update comment")

@comment_router.delete('/{comment_id}/delete')
async def deleteComment(comment_id: str, current_user: str = Depends(get_current_user)):
    try:
        comment = comments_coll.find_one({"_id": ObjectId(comment_id)})
        if not comment:
            raise HTTPException(status_code=404, detail="Comment not found")
        
        if comment["author"] != current_user:
            raise HTTPException(status_code=403, detail="Not authorized to delete this comment")
        
        comments_coll.delete_one({"_id": ObjectId(comment_id)})
        return {"message": "Comment deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to delete comment")

@comment_router.get('/blog/{blog_id}/comments')
async def listComments(blog_id: str, page: int = 1, page_size: int = 5):
    try:
        comments = comments_coll.find({"blog_id": blog_id}).skip((page - 1) * page_size).limit(page_size)
        comment_list = await comments.to_list(length=page_size)
        return CommentsList(comments=comment_list, total=comments_coll.count_documents({"blog_id": blog_id}))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to fetch comments")
