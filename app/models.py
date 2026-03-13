# app/models.py
from sqlalchemy import Column, Integer, String, Float, DateTime, Text, Boolean, ForeignKey, func
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    """User model for database"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    age = Column(Integer, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    posts = relationship("Post", back_populates="user")

    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', email='{self.email}')>"


class ProcessedData(Base):
    """Model to store processed data results"""
    __tablename__ = "processed_data"

    id = Column(Integer, primary_key=True, index=True)
    total = Column(Float, nullable=False)
    average = Column(Float, nullable=False)
    maximum = Column(Float, nullable=False)
    minimum = Column(Float, nullable=False)
    count = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<ProcessedData(id={self.id}, count={self.count}, average={self.average})>"

class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    views = Column(Integer, default=0)
    published = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    # Relationship back to User
    user = relationship("User", back_populates="posts")