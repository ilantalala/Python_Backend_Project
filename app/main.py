from fastapi import FastAPI,Depends
from . import models
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from .database import engine,get_db
from .routers import post,user,auth,vote 
# models.Base.metadata.create_all(bind=engine)
app=FastAPI()
origin=["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origin,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)
@app.get('/')
def root():
    return {"message":"hello world"}
def test_posts(db:Session=Depends(get_db)):
    posts=db.query(models.Post).all()
    return posts