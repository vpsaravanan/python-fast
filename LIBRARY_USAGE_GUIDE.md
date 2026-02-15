# 📚 Library Usage Guide - Where Each Package is Used

This guide shows exactly where each library from `requirements.txt` is being used in your application.

## ✅ Currently Active Libraries

### 1. **FastAPI** (`fastapi==0.100.0`)
**Location**: `app/main.py` - Lines 2-3, 21-27

```python
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse

# Initialize FastAPI app
app = FastAPI(
    title="Python Data Processing API",
    description="A FastAPI application...",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)
```

**Used For**:
- Creating the web application framework
- Defining API routes with decorators (@app.get, @app.post)
- Automatic API documentation generation
- Request/response handling
- Error handling (HTTPException)

**Example Usage in Your Code**:
```python
@app.get("/")                          # Line 100
@app.get("/health")                    # Line 157
@app.post("/process")                  # Line 169
@app.get("/fibonacci/{n}")             # Line 181
```

---

### 2. **Uvicorn** (`uvicorn[standard]==0.23.1`)
**Location**: Docker command & `app/main.py` line 246

```python
# At the bottom of main.py
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

**Command in docker-compose.yml**:
```yaml
command: uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

**Used For**:
- ASGI server that runs the FastAPI application
- Serves HTTP requests on port 8000
- Hot-reload functionality (--reload flag)
- High-performance async request handling

**Why It's Essential**: 
FastAPI needs an ASGI server to actually run. Uvicorn is that server.

---

### 3. **Pydantic** (`pydantic==2.0.3`)
**Location**: `app/main.py` - Lines 4, 32-59

```python
from pydantic import BaseModel, Field

# Pydantic models for request/response validation
class ProcessDataRequest(BaseModel):
    data: List[float] = Field(..., description="List of numbers", example=[10, 20, 30])

class Statistics(BaseModel):
    total: float
    average: float
    max: float
    min: float
    count: int

class ProcessDataResponse(BaseModel):
    timestamp: str
    statistics: Statistics
    fibonacci_sequence: List[int]
    processed: bool

class HealthResponse(BaseModel):
    status: str
    uptime: str
    timestamp: str

class FibonacciResponse(BaseModel):
    n: int
    result: int
    timestamp: str
```

**Used For**:
- Data validation (ensures correct data types)
- Request body validation
- Response schema definition
- Automatic API documentation with examples
- Type checking and conversion

**Example**: When you POST to `/process`:
```json
{
  "data": [10, 20, 30]  ← Pydantic validates this is a list of numbers
}
```

---

### 4. **psycopg2-binary** (`psycopg2-binary==2.9.6`)
**Location**: NOT YET USED - Ready for PostgreSQL integration

**Purpose**: PostgreSQL database adapter for Python

**How to Use It** (Example):
```python
# Add this to main.py when you need database
import psycopg2

# Connect to PostgreSQL
conn = psycopg2.connect(
    host="postgres",
    database="pythondb",
    user="pythonuser",
    password="pythonpass"
)

# Create a route that uses the database
@app.get("/users")
def get_users():
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    return {"users": users}
```

**Your PostgreSQL is already running**: `docker-compose up postgres`
- Host: `postgres` (inside Docker) or `localhost` (from your machine)
- Port: `5432`
- Database: `pythondb`
- User: `pythonuser`
- Password: `pythonpass`

---

### 5. **SQLAlchemy** (`sqlalchemy==2.0.17`)
**Location**: NOT YET USED - Ready for ORM (Object-Relational Mapping)

**Purpose**: Database ORM - Maps Python classes to database tables

**How to Use It** (Example):
```python
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Database connection
DATABASE_URL = "postgresql://pythonuser:pythonpass@postgres:5432/pythondb"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

# Define a model
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)

# Create tables
Base.metadata.create_all(bind=engine)

# Use in a route
@app.get("/users")
def get_users():
    db = SessionLocal()
    users = db.query(User).all()
    return {"users": users}
```

---

### 6. **pytest** (`pytest==7.3.2`)
**Location**: NOT YET USED - For writing tests

**Purpose**: Testing framework

**How to Use It** (Example):
Create `tests/test_main.py`:
```python
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_fibonacci_endpoint():
    response = client.get("/fibonacci/10")
    assert response.status_code == 200
    assert response.json()["result"] == 55

def test_process_endpoint():
    response = client.post("/process", json={"data": [10, 20, 30]})
    assert response.status_code == 200
    assert response.json()["statistics"]["average"] == 20
```

**Run tests**:
```bash
pytest tests/
```

---

### 7. **pytest-asyncio** (`pytest-asyncio==0.21.0`)
**Location**: NOT YET USED - For testing async functions

**Purpose**: Testing async/await code

**Example**:
```python
import pytest

@pytest.mark.asyncio
async def test_async_function():
    result = await some_async_function()
    assert result == expected_value
```

---

### 8. **python-dotenv** (`python-dotenv==1.0.0`)
**Location**: NOT YET USED - For environment variables

**Purpose**: Load environment variables from `.env` file

**How to Use It**:

Create `.env` file:
```env
DATABASE_URL=postgresql://pythonuser:pythonpass@postgres:5432/pythondb
SECRET_KEY=your-secret-key-here
DEBUG=True
```

In `main.py`:
```python
from dotenv import load_dotenv
import os

load_dotenv()  # Load .env file

DATABASE_URL = os.getenv("DATABASE_URL")
SECRET_KEY = os.getenv("SECRET_KEY")
DEBUG = os.getenv("DEBUG") == "True"
```

---

### 9. **click** (`click==8.1.4`)
**Location**: NOT YET USED - For CLI commands

**Purpose**: Create command-line interfaces

**Example**:
Create `cli.py`:
```python
import click

@click.command()
@click.option('--name', default='World', help='Name to greet')
def greet(name):
    """Simple program that greets NAME."""
    click.echo(f'Hello {name}!')

if __name__ == '__main__':
    greet()
```

Run:
```bash
python cli.py --name=John
```

---

## 📊 Library Usage Summary

| Library | Status | Used In | Purpose |
|---------|--------|---------|---------|
| **fastapi** | ✅ Active | `main.py` | Web framework, API routes |
| **uvicorn** | ✅ Active | Docker command, `main.py` | ASGI server |
| **pydantic** | ✅ Active | `main.py` | Data validation, schemas |
| **psycopg2-binary** | 🟡 Ready | Not yet | PostgreSQL driver |
| **sqlalchemy** | 🟡 Ready | Not yet | Database ORM |
| **pytest** | 🟡 Ready | Not yet | Testing framework |
| **pytest-asyncio** | 🟡 Ready | Not yet | Async testing |
| **python-dotenv** | 🟡 Ready | Not yet | Environment variables |
| **click** | 🟡 Ready | Not yet | CLI commands |

---

## 🎯 How Libraries Are Loaded

### When Docker Starts:

1. **Build Stage** (in Dockerfile):
   ```dockerfile
   COPY requirements.txt .
   RUN pip install --no-cache-dir -r requirements.txt
   ```
   - All libraries from `requirements.txt` are installed into the Docker container
   - They're available for your Python code to import

2. **Runtime**:
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000 --reload
   ```
   - Uvicorn starts and imports `main.py`
   - Python imports all libraries at the top of `main.py`
   - FastAPI app initializes
   - Routes become available

### Import Order in main.py:
```python
from fastapi import ...          # Line 2
from fastapi.responses import ... # Line 3
from pydantic import ...          # Line 4
from typing import ...            # Line 5 (Python built-in)
import logging                    # Line 6 (Python built-in)
from datetime import ...          # Line 7 (Python built-in)
import sys                        # Line 8 (Python built-in)
```

---

## 🔨 Next Steps - Using More Libraries

### Example 1: Add Database Support
```python
# Add to main.py
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://pythonuser:pythonpass@postgres:5432/pythondb"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

@app.post("/save-data")
def save_data(request: ProcessDataRequest):
    # Save to database
    pass
```

### Example 2: Add Environment Variables
```python
# Add to main.py
from dotenv import load_dotenv
import os

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY", "default-secret")
```

### Example 3: Add Tests
```bash
# Create tests/test_api.py
pytest tests/test_api.py
```

---

## 📖 Want to See It in Action?

Your application is running at: **http://localhost:8000**

- Visit `/docs` to see how Pydantic models create the API documentation
- Try the `/process` endpoint to see data validation in action
- Check the terminal logs to see uvicorn serving requests

All the libraries work together to create your FastAPI application! 🚀
