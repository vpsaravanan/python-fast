# app.py - example usage
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from redis_client import redis_client
from database import get_db
from models import User
# import time
# import os

redisrouter = APIRouter()
@redisrouter.get('/redis_test')


# Store data
# redis_client.set('user:1', 'John Doe', ex=3600)  # expires in 1 hour

# Retrieve data
# user = redis_client.get('user:1')

# Cache example
def get_user(user_id, db: Session = Depends(get_db)):
    # Try cache first
    print(user_id)
    cached = redis_client.get(f'user:{user_id}')
    if cached:
        print ("return from cache")
        return cached
    
    # Get from DB (your existing code)
    user = db.query(User).get(user_id)
    print(user)
    
    # Store in cache
    redis_client.setex(f'user:{user_id}', 3600, user.username)
    return user

