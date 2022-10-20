from fastapi import FastAPI, HTTPException
from sqlalchemy import desc
from sqlalchemy.sql.functions import count

from database import SessionLocal
from schema import UserGet, PostGet, FeedGet
from table_feed import Feed
from table_post import Post
from table_user import User
from typing import List

app=FastAPI()

@app.get("/user/{id}", response_model=UserGet)
def select(id):
    session=SessionLocal()
    result=session.query(User).filter(id==User.id).first()
    if not result:
        raise HTTPException(404)
    else:
        return result

@app.get("/post/{id}", response_model=PostGet)
def select(id):
    session=SessionLocal()
    result=session.query(Post).filter(id==Post.id).first()
    if not result:
        raise HTTPException(404)
    else:
        return result

@app.get("/user/{id}/feed", response_model=List[FeedGet])
def get(id, limit=10):
    session=SessionLocal()
    result=session.query(Feed).filter(id==Feed.user_id).order_by(desc(Feed.time)).limit(limit).all()
    return result

@app.get("/post/{id}/feed", response_model=List[FeedGet])
def get(id, limit=10):
    session=SessionLocal()
    result=session.query(Feed).filter(id==Feed.post_id).order_by(desc(Feed.time)).limit(limit).all()
    return result

@app.get("/post/recommendations/", response_model=List[PostGet])
def recomend(id:int, limit:int=10):
    session=SessionLocal()
    result=session.query(Post).filter(Feed.action=='like').filter(Feed.post_id==Post.id).group_by(Post.id).order_by(desc(count(Post.id)))\
        .limit(limit)\
        .all()
    return result
