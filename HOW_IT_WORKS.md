# 🔄 How Your Application Works - Complete Flow

## 📦 Step 1: Docker Build Process

```
┌─────────────────────────────────────────────────────────────┐
│  docker-compose up --build python-app                       │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│  Dockerfile Execution:                                      │
│  ┌───────────────────────────────────────────────────────┐ │
│  │ FROM python:3.11-slim                                 │ │
│  │ WORKDIR /app                                          │ │
│  │ COPY requirements.txt .                               │ │
│  │ RUN pip install -r requirements.txt  ← INSTALLS LIBS │ │
│  │ COPY . .                                              │ │
│  └───────────────────────────────────────────────────────┘ │
│                                                             │
│  All libraries from requirements.txt are now installed:    │
│  ✓ fastapi                                                  │
│  ✓ uvicorn                                                  │
│  ✓ pydantic                                                 │
│  ✓ psycopg2-binary                                          │
│  ✓ sqlalchemy                                               │
│  ✓ pytest                                                   │
│  ✓ python-dotenv                                            │
│  ✓ click                                                    │
└─────────────────────────────────────────────────────────────┘
```

## 🚀 Step 2: Application Startup

```
┌─────────────────────────────────────────────────────────────┐
│  Command: uvicorn main:app --host 0.0.0.0 --port 8000      │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│  Uvicorn starts and imports main.py                         │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│  main.py Line-by-Line Execution:                            │
│                                                              │
│  Line 2:  from fastapi import FastAPI, HTTPException        │
│           ↓ Imports FastAPI library                         │
│                                                              │
│  Line 3:  from fastapi.responses import HTMLResponse        │
│           ↓ Imports HTML response handler                   │
│                                                              │
│  Line 4:  from pydantic import BaseModel, Field             │
│           ↓ Imports data validation                         │
│                                                              │
│  Line 21: app = FastAPI(...)                                │
│           ↓ Creates FastAPI application instance            │
│                                                              │
│  Line 32-59: Define Pydantic models                         │
│           ↓ Creates data schemas                            │
│                                                              │
│  Line 100: @app.get("/")                                    │
│           ↓ Registers route handlers                        │
│                                                              │
│  Line 157: @app.get("/health")                              │
│  Line 169: @app.post("/process")                            │
│  Line 181: @app.get("/fibonacci/{n}")                       │
│                                                              │
│  Line 235: @app.on_event("startup")                         │
│           ↓ Runs startup tasks                              │
└─────────────────────────────────────────────────────────────┘
```

## 🌐 Step 3: Request Handling Flow

```
User Browser/Client
       │
       │ HTTP Request: GET http://localhost:8000/health
       │
       ▼
┌─────────────────────────────────────────────────────────────┐
│  UVICORN (Port 8000)                                        │
│  ← Receives HTTP request                                    │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│  FASTAPI Router                                             │
│  ← Matches URL "/health" to route handler                   │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│  @app.get("/health")                                        │
│  async def health_check():                                  │
│      return HealthResponse(...)                             │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│  PYDANTIC Validation                                        │
│  ← Validates response matches HealthResponse model          │
│  ← Converts Python dict to JSON                             │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│  UVICORN                                                    │
│  ← Sends HTTP response back                                 │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
               User Browser
         Receives JSON Response:
         {
           "status": "healthy",
           "uptime": "0:05:23",
           "timestamp": "2025-12-10..."
         }
```

## 📝 Detailed Example: POST /process Request

```
Step 1: User sends POST request
────────────────────────────────
POST http://localhost:8000/process
Content-Type: application/json

{
  "data": [10, 20, 30, 40, 50]
}

        │
        ▼

Step 2: Uvicorn receives request
────────────────────────────────
✓ Receives HTTP POST
✓ Reads request body
✓ Routes to FastAPI

        │
        ▼

Step 3: FastAPI processes request
────────────────────────────────
✓ Matches route: @app.post("/process")
✓ Extracts JSON body

        │
        ▼

Step 4: Pydantic validates input
────────────────────────────────
from pydantic import BaseModel

class ProcessDataRequest(BaseModel):
    data: List[float]

✓ Validates "data" is a list
✓ Validates all items are numbers
✓ Converts to Python types
✗ If invalid → Returns 422 Error

        │
        ▼

Step 5: Route handler executes
────────────────────────────────
@app.post("/process")
async def process_endpoint(request: ProcessDataRequest):
    return process_data(request.data)

✓ Calls process_data() function
✓ Calculates statistics
✓ Generates Fibonacci sequence

        │
        ▼

Step 6: Returns ProcessDataResponse
────────────────────────────────
class ProcessDataResponse(BaseModel):
    timestamp: str
    statistics: Statistics
    fibonacci_sequence: List[int]
    processed: bool

✓ Pydantic validates output
✓ Converts to JSON

        │
        ▼

Step 7: Response sent to user
────────────────────────────────
HTTP 200 OK
Content-Type: application/json

{
  "timestamp": "2025-12-10T12:30:00",
  "statistics": {
    "total": 150,
    "average": 30,
    "max": 50,
    "min": 10,
    "count": 5
  },
  "fibonacci_sequence": [0, 1, 1, 2, 3],
  "processed": true
}
```

## 🔍 Where Each Library is Active

```
┌─────────────────────────────────────────────────────────────┐
│  YOUR REQUEST JOURNEY                                       │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  1. Browser → http://localhost:8000/health                  │
│                                                              │
│  2. Docker Container (Port 8000)                            │
│     └─ UVICORN 📦                                           │
│        │ ✓ Listening on port 8000                           │
│        │ ✓ Handles HTTP protocol                            │
│        │ ✓ Manages connections                              │
│        └─ Passes request to FastAPI                         │
│                                                              │
│  3. FastAPI App 📦                                          │
│     └─ from fastapi import FastAPI                          │
│        │ ✓ Routes requests to handlers                      │
│        │ ✓ Injects dependencies                             │
│        │ ✓ Handles errors                                   │
│        │ ✓ Generates /docs & /redoc                         │
│        └─ Calls your route function                         │
│                                                              │
│  4. Your Route Handler                                      │
│     └─ @app.get("/health")                                  │
│        │ ✓ Executes your code                               │
│        │ ✓ Returns HealthResponse object                    │
│        └─ Passes to Pydantic                                │
│                                                              │
│  5. Pydantic Validation 📦                                  │
│     └─ from pydantic import BaseModel                       │
│        │ ✓ Validates response structure                     │
│        │ ✓ Checks data types                                │
│        │ ✓ Serializes to JSON                               │
│        └─ Returns to FastAPI                                │
│                                                              │
│  6. FastAPI → Uvicorn → Browser                            │
│     └─ JSON Response sent back                              │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## 📚 Libraries NOT YET Active (But Ready!)

```
┌─────────────────────────────────────────────────────────────┐
│  🟡 READY BUT NOT USED YET                                  │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  psycopg2-binary  → PostgreSQL driver                       │
│    └─ Add: import psycopg2                                  │
│    └─ Use: conn = psycopg2.connect(...)                     │
│                                                              │
│  sqlalchemy       → Database ORM                            │
│    └─ Add: from sqlalchemy import create_engine            │
│    └─ Use: engine = create_engine(DATABASE_URL)            │
│                                                              │
│  pytest           → Testing framework                       │
│    └─ Add: tests/test_main.py                              │
│    └─ Run: pytest                                           │
│                                                              │
│  python-dotenv    → Environment variables                   │
│    └─ Add: from dotenv import load_dotenv                  │
│    └─ Use: load_dotenv()                                    │
│                                                              │
│  click            → CLI commands                            │
│    └─ Add: import click                                     │
│    └─ Use: @click.command()                                 │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## 🎯 Summary

**Currently Active in Your App:**
1. ✅ **Uvicorn** - Runs the web server on port 8000
2. ✅ **FastAPI** - Handles routing and API logic
3. ✅ **Pydantic** - Validates all input/output data

**The code path for every request:**
```
Browser → Uvicorn → FastAPI → Your Code → Pydantic → FastAPI → Uvicorn → Browser
          (HTTP)   (Routing)  (Logic)    (Validate)  (JSON)     (HTTP)
```

**Where libraries are imported:**
- All imports are at the top of `app/main.py` (lines 2-8)
- Python loads them when the app starts
- They stay in memory for the entire application lifetime

**Want to use more libraries?**
- They're already installed in your Docker container
- Just add import statements to your code
- See LIBRARY_USAGE_GUIDE.md for examples

Your application is like a restaurant:
- **Uvicorn** = The front door (takes orders)
- **FastAPI** = The manager (routes orders to kitchen)
- **Your routes** = The chefs (make the food)
- **Pydantic** = Quality control (checks everything is correct)
- **Other libraries** = Kitchen equipment (ready when you need them)

🚀 Everything is working perfectly!
