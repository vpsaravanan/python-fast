# 🔍 How to View FastAPI Source Code in Docker Container

## ✅ FastAPI Source Code Location

**Inside Docker Container:**
```
/usr/local/lib/python3.11/site-packages/fastapi/
```

**On Your Local Machine (Already Copied):**
```
./fastapi_source_code/
```

---

## 📂 FastAPI Source Code Structure

```
fastapi_source_code/
├── __init__.py              (30 lines)    - Main entry point, exports
├── applications.py          (1,051 lines) - FastAPI class definition
├── routing.py               (1,556 lines) - APIRouter, route handling
├── params.py                (688 lines)   - Query, Path, Body params
├── param_functions.py       (438 lines)   - Parameter functions
├── responses.py             (29 lines)    - Response classes
├── requests.py              (4 lines)     - Request class
├── exceptions.py            (46 lines)    - HTTPException
├── encoders.py              (181 lines)   - JSON encoders
├── utils.py                 (228 lines)   - Utility functions
├── _compat.py               (616 lines)   - Compatibility layer
├── concurrency.py           (38 lines)    - Async helpers
├── datastructures.py        (84 lines)    - Data structures
├── background.py            (2 lines)     - Background tasks
├── websockets.py            (3 lines)     - WebSocket support
├── testclient.py            (1 line)      - Test client
├── dependencies/            - Dependency injection
│   ├── models.py
│   └── utils.py
├── middleware/              - Middleware components
│   ├── cors.py
│   ├── gzip.py
│   ├── httpsredirect.py
│   └── trustedhost.py
├── openapi/                 - OpenAPI/Swagger docs
│   ├── constants.py
│   ├── docs.py
│   ├── models.py
│   └── utils.py
└── security/                - Security utilities
    ├── api_key.py
    ├── http.py
    ├── oauth2.py
    └── open_id_connect_url.py

Total: ~5,000 lines of code
```

---

## 🎯 Methods to Access FastAPI Source Code

### Method 1: Browse Locally in VS Code (✅ Already Done!)

```bash
# I already copied it for you!
code ./fastapi_source_code
```

**The source code is now at:** `/Users/saravana/Documents/python/fastapi_source_code/`

You can now browse it directly in VS Code!

---

### Method 2: View Files from Terminal

```bash
# View the main FastAPI class
cat fastapi_source_code/applications.py

# View routing logic
cat fastapi_source_code/routing.py

# View parameter handling
cat fastapi_source_code/params.py

# Search for specific code
grep -n "class FastAPI" fastapi_source_code/applications.py
grep -n "def get" fastapi_source_code/routing.py
```

---

### Method 3: Access Container Shell Interactively

```bash
# Enter the container
docker exec -it python-python-app-1 /bin/bash

# Once inside, navigate to FastAPI source
cd /usr/local/lib/python3.11/site-packages/fastapi

# List files
ls -la

# View any file
cat __init__.py
cat applications.py
less routing.py

# Exit container
exit
```

---

### Method 4: View Files Directly from Container

```bash
# View FastAPI main initialization
docker exec python-python-app-1 cat /usr/local/lib/python3.11/site-packages/fastapi/__init__.py

# View FastAPI application class
docker exec python-python-app-1 cat /usr/local/lib/python3.11/site-packages/fastapi/applications.py

# View routing logic
docker exec python-python-app-1 cat /usr/local/lib/python3.11/site-packages/fastapi/routing.py
```

---

### Method 5: Use Python Inspect Module

```bash
# View FastAPI class source code
docker exec python-python-app-1 python -c "
import inspect
import fastapi
print(inspect.getsource(fastapi.FastAPI))
"

# View a specific method
docker exec python-python-app-1 python -c "
import inspect
from fastapi import FastAPI
app = FastAPI()
print(inspect.getsource(app.get))
"

# List all FastAPI attributes
docker exec python-python-app-1 python -c "
import fastapi
print(dir(fastapi))
"
```

---

### Method 6: Interactive Python in Container

```bash
# Start Python shell in container
docker exec -it python-python-app-1 python

# Then in Python shell:
>>> import fastapi
>>> import inspect
>>> 
>>> # View source of FastAPI class
>>> print(inspect.getsource(fastapi.FastAPI))
>>> 
>>> # View specific method
>>> print(inspect.getsource(fastapi.FastAPI.get))
>>> 
>>> # View file location
>>> print(fastapi.__file__)
>>> 
>>> # Exit
>>> exit()
```

---

## 🔑 Key Files to Explore

### 1. **applications.py** - The FastAPI Class

This is where the main `FastAPI` class is defined. When you do:
```python
app = FastAPI()
```

This is calling the class from `applications.py`.

**To view:**
```bash
cat fastapi_source_code/applications.py | head -100
```

**Key sections:**
- `class FastAPI(Starlette)` - Main application class
- `def get()` - GET route decorator
- `def post()` - POST route decorator
- `def include_router()` - Include sub-routers

---

### 2. **routing.py** - Route Handling

This file handles all the routing logic, including:
- `APIRouter` class
- Route matching
- Dependency injection
- Request/response handling

**To view:**
```bash
cat fastapi_source_code/routing.py | head -100
```

---

### 3. **params.py** - Parameter Definitions

Defines `Query`, `Path`, `Body`, `Header`, `Cookie` parameters.

**To view:**
```bash
cat fastapi_source_code/params.py | head -50
```

---

### 4. **__init__.py** - Main Entry Point

This is what gets imported when you do `from fastapi import FastAPI`.

**To view:**
```bash
cat fastapi_source_code/__init__.py
```

You'll see it imports from other files:
```python
from .applications import FastAPI as FastAPI
from .exceptions import HTTPException as HTTPException
from .routing import APIRouter as APIRouter
```

---

## 🔬 Understanding How Your Code Uses FastAPI

### Example 1: When you import FastAPI

**Your code:**
```python
from fastapi import FastAPI, HTTPException
```

**What happens:**
1. Python loads `fastapi/__init__.py`
2. `__init__.py` imports from `fastapi/applications.py`
3. `FastAPI` class and `HTTPException` are now available

**See the source:**
```bash
# View the imports
cat fastapi_source_code/__init__.py

# View the FastAPI class definition
cat fastapi_source_code/applications.py | grep -A 50 "class FastAPI"
```

---

### Example 2: When you create routes

**Your code:**
```python
@app.get("/health")
async def health_check():
    return {"status": "healthy"}
```

**What happens:**
1. `@app.get()` calls the `get()` method in `applications.py`
2. Which calls `add_api_route()` in `routing.py`
3. Route is registered in the router

**See the source:**
```bash
# View the get() decorator method
grep -A 20 "def get(" fastapi_source_code/applications.py

# View the route registration
grep -A 30 "def add_api_route" fastapi_source_code/routing.py
```

---

### Example 3: When you use Pydantic models

**Your code:**
```python
from pydantic import BaseModel

class ProcessDataRequest(BaseModel):
    data: List[float]
```

**What happens:**
1. FastAPI uses Pydantic for validation
2. When a request comes in, `routing.py` validates it
3. Uses encoders from `encoders.py` for JSON conversion

**See the source:**
```bash
# View how FastAPI uses Pydantic
grep -n "pydantic" fastapi_source_code/routing.py | head -10

# View JSON encoding
cat fastapi_source_code/encoders.py | head -50
```

---

## 🎓 Practical Examples

### Example 1: Find how @app.get() works

```bash
# Search for the get method definition
grep -n "def get" fastapi_source_code/applications.py

# View the full method
sed -n '500,600p' fastapi_source_code/applications.py
```

### Example 2: Understand route parameters

```bash
# View Path parameter implementation
grep -A 20 "class Path" fastapi_source_code/params.py

# View Query parameter implementation
grep -A 20 "class Query" fastapi_source_code/params.py
```

### Example 3: See how docs are generated

```bash
# View OpenAPI documentation generation
cat fastapi_source_code/openapi/docs.py

# View OpenAPI models
cat fastapi_source_code/openapi/models.py
```

---

## 📝 Quick Reference Commands

```bash
# Copy FastAPI source to local (already done!)
docker cp python-python-app-1:/usr/local/lib/python3.11/site-packages/fastapi ./fastapi_source_code

# Open in VS Code
code ./fastapi_source_code

# Search for specific functionality
grep -r "HTTPException" fastapi_source_code/
grep -r "APIRouter" fastapi_source_code/
grep -r "def get" fastapi_source_code/

# View line counts
find fastapi_source_code -name "*.py" -exec wc -l {} + | sort -n

# View all Python files
find fastapi_source_code -name "*.py" -type f
```

---

## 🗂️ Other Installed Libraries

You can view source code of other libraries too:

```bash
# Pydantic
docker cp python-python-app-1:/usr/local/lib/python3.11/site-packages/pydantic ./pydantic_source_code

# Uvicorn
docker cp python-python-app-1:/usr/local/lib/python3.11/site-packages/uvicorn ./uvicorn_source_code

# SQLAlchemy
docker cp python-python-app-1:/usr/local/lib/python3.11/site-packages/sqlalchemy ./sqlalchemy_source_code

# All installed packages
docker exec python-python-app-1 pip list
```

---

## 💡 Pro Tips

1. **Use VS Code Search:** Open `fastapi_source_code/` in VS Code and use Cmd+Shift+F to search across all files

2. **Follow the imports:** Start from `__init__.py` and follow the imports to understand the structure

3. **Read the docstrings:** FastAPI has excellent documentation in the source code

4. **Use GitHub:** Visit https://github.com/tiangolo/fastapi for the latest code with syntax highlighting

5. **Check version:** Your container has FastAPI 0.100.0 - make sure to reference the correct version

---

## 🚀 What to Look For

### To understand how routes work:
- `applications.py` - Lines ~400-600 (route decorators)
- `routing.py` - Lines ~200-400 (APIRouter class)

### To understand request validation:
- `routing.py` - Lines ~600-800 (request validation)
- `params.py` - All classes (Query, Path, Body, etc.)

### To understand response handling:
- `routing.py` - Lines ~800-1000 (response handling)
- `encoders.py` - JSON encoding logic

### To understand dependency injection:
- `dependencies/` folder - Entire directory

### To understand automatic docs:
- `openapi/` folder - Entire directory

---

## ✅ Summary

✅ **FastAPI source is now at:** `./fastapi_source_code/`  
✅ **You can browse it in VS Code**  
✅ **Total code:** ~5,000 lines across multiple files  
✅ **Key file:** `applications.py` (the main FastAPI class)  
✅ **Route logic:** `routing.py` (APIRouter and route handling)

**Start exploring:**
```bash
code ./fastapi_source_code
```

Happy exploring! 🎉
