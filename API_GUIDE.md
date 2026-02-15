# FastAPI Application Guide

## 🚀 Quick Start

### Run with Docker
```bash
docker-compose up --build python-app
```

### Run Locally (without Docker)
```bash
cd app
pip install -r ../requirements.txt
uvicorn main:app --reload
```

## 📍 API Endpoints & Routes

### 1. **GET /** - Welcome Page
- **URL**: `http://localhost:8000/`
- **Description**: Beautiful HTML welcome page with API information
- **Response**: HTML page showing status, uptime, and available endpoints

### 2. **GET /health** - Health Check
- **URL**: `http://localhost:8000/health`
- **Description**: Check if the API is running
- **Response**:
```json
{
  "status": "healthy",
  "uptime": "0:05:23",
  "timestamp": "2025-12-10T10:30:00.123456"
}
```

### 3. **POST /process** - Process Data
- **URL**: `http://localhost:8000/process`
- **Description**: Process a list of numbers and get statistics
- **Request Body**:
```json
{
  "data": [10, 20, 30, 40, 50]
}
```
- **Response**:
```json
{
  "timestamp": "2025-12-10T10:30:00.123456",
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

### 4. **GET /fibonacci/{n}** - Calculate Fibonacci
- **URL**: `http://localhost:8000/fibonacci/10`
- **Description**: Calculate the nth Fibonacci number
- **Response**:
```json
{
  "n": 10,
  "result": 55,
  "timestamp": "2025-12-10T10:30:00.123456"
}
```

## 📚 Interactive Documentation

### Swagger UI (Recommended)
- **URL**: `http://localhost:8000/docs`
- **Features**:
  - Try out all endpoints interactively
  - See request/response schemas
  - Test with different parameters

### ReDoc
- **URL**: `http://localhost:8000/redoc`
- **Features**:
  - Clean, readable documentation
  - Better for reading/reference

## 🧪 Testing the API

### Using cURL

**Health Check:**
```bash
curl http://localhost:8000/health
```

**Process Data:**
```bash
curl -X POST http://localhost:8000/process \
  -H "Content-Type: application/json" \
  -d '{"data": [10, 20, 30, 40, 50]}'
```

**Calculate Fibonacci:**
```bash
curl http://localhost:8000/fibonacci/10
```

### Using Python requests

```python
import requests

# Health check
response = requests.get("http://localhost:8000/health")
print(response.json())

# Process data
response = requests.post(
    "http://localhost:8000/process",
    json={"data": [10, 20, 30, 40, 50]}
)
print(response.json())

# Calculate Fibonacci
response = requests.get("http://localhost:8000/fibonacci/10")
print(response.json())
```

### Using JavaScript (fetch)

```javascript
// Health check
fetch('http://localhost:8000/health')
  .then(response => response.json())
  .then(data => console.log(data));

// Process data
fetch('http://localhost:8000/process', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ data: [10, 20, 30, 40, 50] })
})
  .then(response => response.json())
  .then(data => console.log(data));
```

## 🔧 Configuration

- **Port**: 8000 (configurable in docker-compose.yml)
- **Auto-reload**: Enabled (changes to code will auto-restart the server)
- **Logging**: Logs are written to `app/app.log` and console

## 📦 What's Included

- ✅ **FastAPI Framework** - Modern, fast web framework
- ✅ **Pydantic Models** - Request/response validation
- ✅ **Automatic API Docs** - Swagger UI & ReDoc
- ✅ **Logging** - File and console logging
- ✅ **Type Hints** - Full Python type annotations
- ✅ **Error Handling** - Proper HTTP error responses
- ✅ **Docker Support** - Ready to deploy

## 🎯 Next Steps

1. Start the application: `docker-compose up --build python-app`
2. Visit: `http://localhost:8000/`
3. Try the interactive docs: `http://localhost:8000/docs`
4. Test the endpoints with the examples above

## 🗄️ Database Integration

Your PostgreSQL database is already configured in docker-compose.yml. To connect:

```python
# Add to requirements.txt: sqlalchemy, psycopg2-binary
from sqlalchemy import create_engine

DATABASE_URL = "postgresql://pythonuser:pythonpass@postgres:5432/pythondb"
engine = create_engine(DATABASE_URL)
```

## 🚀 Production Deployment

For production, update the command in docker-compose.yml:
```yaml
command: uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

Happy coding! 🎉
