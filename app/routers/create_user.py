# from fastapi import APIRouter

# router = APIRouter()

# @router.get("/create-user")
# def create_user(username: str, email: str, age: int = 18):
#     user = {"username": username, "email": email, "age": age}
#     return {"message": "User created successfully", "user": user}


# from fastapi import APIRouter, Query
# from typing import Optional

# router = APIRouter()

# @router.post("/create-user")
# async def create_user(
#     username: str = Query(..., description="Username for the new user"),
#     email: str = Query(..., description="Email address"),
#     age: Optional[int] = Query(18, description="Age of the user", ge=0, le=150)
# ):
#     # Business logic here
#     user_data = {
#         "username": username,
#         "email": email,
#         "age": age
#     }
    
#     # Simulate saving to database
#     # save_to_database(user_data)
    
#     return {
#         "status": "success",
#         "message": f"User '{username}' created successfully",
#         "data": user_data
#     }
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import User
from pydantic import BaseModel, EmailStr
import sqlalchemy

class UserCreate(BaseModel):
    username: str
    email: str
    age: int = 18

router = APIRouter()

@router.post("/create-user")
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    Create a new user in the MySQL database
    
    - **username**: Unique username
    - **email**: User's email address
    - **age**: User's age (default: 18)
    """
    # Check if user already exists
    existing_user = db.query(User).filter(
        (User.username == user.username) | (User.email == user.email)
    ).first()
    
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="User with this username or email already exists"
        )
    
    # Create new user
    new_user = User(username=user.username, email=user.email, age=user.age)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return {
        "message": "User created successfully",
        "user": {
            "id": new_user.id,
            "username": new_user.username,
            "email": new_user.email,
            "age": new_user.age,
            "created_at": new_user.created_at.isoformat() if new_user.created_at else None
        }
    }

@router.get("/users/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    """Get a user by ID"""
    print (sqlalchemy.__version__)
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(status_code=404, detail=sqlalchemy.__version__)
    
    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "age": user.age,
        "created_at": user.created_at.isoformat() if user.created_at else None
    }