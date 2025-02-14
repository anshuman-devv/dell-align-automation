from Application.routes import userRoutes, blogRoutes, commentRoutes
from fastapi import FastAPI     


app = FastAPI()

app.include_router(userRoutes.auth_router, prefix='/auth', tags=['Auth'])
app.include_router(blogRoutes.blog_router, prefix='/blogs', tags=['Blogs'])
app.include_router(commentRoutes.comment_router, prefix='/comments', tags=['Comments'])
