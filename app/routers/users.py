from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import User
import sys
import gc
import copy
import multiprocessing
import time

router = APIRouter()

@router.get("/users")
def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Get all users from the MySQL database
    
    - **skip**: Number of records to skip (for pagination)
    - **limit**: Maximum number of records to return
    """
    # return {"message": "This endpoint will return all users."}
    users = db.query(User).offset(skip).limit(limit).all()
    # data = {"name": "Ram", "age": 30}
    # print(data["name"])   # O(1)
    # s = "hello"
    # print(s[-1])  # O(1)
    # s = "Hello"
    # print(s)
    # s = "hello"
    # print(id(s))     # e.g., 140246726789040
    # s = s + " world"
    # print(id(s))
    # data = bytearray(b'hello')
    # mv = memoryview(data)  # No copy created
    # mv[4] = 73
    # print(data)
    square(5)
    original = [[1, 2], [3, 4]]
    original[1][1] = 11
    shallow = copy.copy(original)
    print(shallow)
    deep = copy.deepcopy(original)
    print(deep)
    return {
        "count": len(users),
        "users": [
            {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "age": user.age,
                "created_at": user.created_at.isoformat() if user.created_at else None
            }
            for user in users
        ]
    }
def square(number):
    """CPU-intensive task: calculate square"""
    result = number * number
    print(f"Process {multiprocessing.current_process().name}: {number}² = {result}")
    time.sleep(0.5)  # Simulate work
    numbers = [1, 2, 3, 4, 5, 6, 7, 8]
    
    print("Sequential execution:")
    start = time.time()
    results_seq = [5 for n in numbers]
    print(f"Time: {time.time() - start:.2f}s\n")
    
    print("Parallel execution (using Pool):")
    start = time.time()
    
    # Create pool with 4 worker processes
    with multiprocessing.Pool(processes=4) as pool:
        results_par = pool.map(square, numbers)
    
    print(f"Time: {time.time() - start:.2f}s")
    print(f"Results: {results_par}")
    return result

if __name__ == "__main__":
    # Numbers to process
    numbers = [1, 2, 3, 4, 5, 6, 7, 8]
    
    print("Sequential execution:")
    start = time.time()
    results_seq = [square(n) for n in numbers]
    print(f"Time: {time.time() - start:.2f}s\n")
    
    print("Parallel execution (using Pool):")
    start = time.time()
    
    # Create pool with 4 worker processes
    with multiprocessing.Pool(processes=4) as pool:
        results_par = pool.map(square, numbers)
    
    print(f"Time: {time.time() - start:.2f}s")
    print(f"Results: {results_par}")