from fastapi import APIRouter, HTTPException
from Application.config.db import userdb,  coll, userdb
from Application.auth.hashing import verify_password, hash_password
from Application.models.user import UserCreate, UserLogin, TokenResponse, UserResponse
from Application.routes.auth import create_access_token
from bson import ObjectId


auth_router = APIRouter()

def check_author(blog_id: str, current_user: str):
    blog = coll.find_one({"_id": ObjectId(blog_id)})
    if blog["author"] != current_user:
        raise HTTPException(status_code=403, detail="You are not authorized to perform this action")

@auth_router.post("/signup", response_model=UserResponse)
async def signup(user: UserCreate):
    existing = userdb.find_one({"email": user.email})
    if existing:
        raise HTTPException(status_code=400, detail="Email already exists")
    
    user_dict = user.model_dump()
    hashed_password = hash_password(user.password)
    user_dict["hashed_password"] = hashed_password
    user = userdb.insert_one(user_dict) 
    # user_dict = user.dict()
    user_dict["id"] = str(user.inserted_id)

    return UserResponse(**user_dict)


@auth_router.post("/login", response_model=TokenResponse)
async def login(user: UserLogin):
    db_user = userdb.find_one({"email": user.email})
    if not db_user or not verify_password(user.password, db_user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    access_token = create_access_token(data={"sub": str(db_user["_id"])})
    return {"access_token": access_token, "token_type": "bearer"}