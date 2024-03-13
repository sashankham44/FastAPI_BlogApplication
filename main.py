import logging
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from pydantic import BaseModel
from database import AsyncSessionLocal, engine
from models import User, Post
from database import Base
from sqlalchemy.exc import SQLAlchemyError


logging.basicConfig(level=logging.INFO)

app = FastAPI()


@app.on_event("startup")
async def startup():
    async with AsyncSessionLocal() as session:
        try:
            # Try to execute a simple query to check the database connection
            await session.execute('SELECT 1')
            await session.commit()
            logging.info("Successfully connected to the database.")
        except SQLAlchemyError as e:
            logging.error(f"Failed to connect to the database: {e}")

            

# Define Pydantic models for request and response validation
class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    pass

class UserResponse(UserBase):
    id: int
    class Config:
        orm_mode = True

class PostBase(BaseModel):
    title: str
    content: str

class PostCreate(PostBase):
    user_id: int

class PostResponse(PostBase):
    id: int
    user_id: int
    class Config:
        orm_mode = True

# Dependency for async DB sessions
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        # Create the tables if they don't exist
        await conn.run_sync(Base.metadata.create_all)

# CRUD operations for Users
@app.post("/users/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    new_user = User(username=user.username)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

@app.get("/users/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).filter_by(id=user_id))
    user = result.scalars().first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# CRUD operations for Posts
@app.post("/posts/", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
async def create_post(post: PostCreate, db: AsyncSession = Depends(get_db)):
    new_post = Post(**post.dict())
    db.add(new_post)
    await db.commit()
    await db.refresh(new_post)
    return new_post

@app.get("/posts/{post_id}", response_model=PostResponse, status_code=status.HTTP_200_OK)
async def get_post(post_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Post).filter_by(id=post_id))
    post = result.scalars().first()
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return post

@app.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(post_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Post).filter_by(id=post_id))
    post = result.scalars().first()
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    await db.delete(post)
    await db.commit()
    return {"detail": "Post deleted successfully"}