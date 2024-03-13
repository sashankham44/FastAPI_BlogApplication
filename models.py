from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True)

class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100))
    content = Column(String(255))
    user_id = Column(Integer, ForeignKey('users.id'))

    user = relationship("User", back_populates="posts")

# Establish the relationship on the User side
User.posts = relationship("Post", order_by=Post.id, back_populates="user")