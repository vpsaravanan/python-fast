# app/main.py
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field
from typing import List, Optional
import typing
import logging
from datetime import datetime
import sys
import site
from routers import users
from routers import create_user
from test import test

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('app.log')
    ]
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Python Data Processing API",
    description="A FastAPI application for data processing, statistics calculation, and Fibonacci sequences",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Application startup time
start_time = datetime.now()

# Pydantic models for request/response validation
class ProcessDataRequest(BaseModel):
    data: List[float] = Field(..., description="List of numbers to process", example=[10, 20, 30, 40, 50])

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
    output: str

class FibonacciResponse(BaseModel):
    n: int
    result: int
    timestamp: str

# Utility functions
def calculate_fibonacci(n: int) -> int:
    """Calculate Fibonacci number"""
    if n < 0:
        raise ValueError("n must be non-negative")
    if n <= 1:
        return n
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b

def process_data(data: List[float]) -> ProcessDataResponse:
    """Process data and calculate statistics"""
    try:
        logger.info(f"Processing {len(data)} items")
        
        if not data:
            raise ValueError("Data list cannot be empty")
        
        # Calculate statistics
        total = sum(data)
        average = total / len(data)
        maximum = max(data)
        minimum = min(data)
        
        # Generate Fibonacci sequence
        fib_sequence = [calculate_fibonacci(i) for i in range(min(10, len(data)))]
        
        result = ProcessDataResponse(
            timestamp=datetime.now().isoformat(),
            statistics=Statistics(
                total=total,
                average=average,
                max=maximum,
                min=minimum,
                count=len(data)
            ),
            fibonacci_sequence=fib_sequence,
            processed=True
        )
        
        logger.info(f"Data processed successfully: {result.statistics}")
        return result
        
    except Exception as e:
        logger.error(f"Error processing data: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

# Initialize test value at startup
test().get_value()  
logger.info(f"Test value initialized: {test().get_value()}")

app.include_router(users.router)
app.include_router(create_user.router)

# API Routes
# @app.get("/", response_class=HTMLResponse)
# @app.get("/")
# async def root():
#     """Welcome page with API information"""
#     uptime = datetime.now() - start_time
#     html_content = f"""
#     <!DOCTYPE html>
#     <html>
#     <head>
#         <title>Python Data Processing API</title>
#         <style>
#             body {{
#                 font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
#                 max-width: 800px;
#                 margin: 50px auto;
#                 padding: 20px;
#                 background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
#                 color: white;
#             }}
#             .container {{
#                 background: rgba(255, 255, 255, 0.1);
#                 border-radius: 10px;
#                 padding: 30px;
#                 backdrop-filter: blur(10px);
#             }}
#             h1 {{
#                 color: #fff;
#                 text-align: center;
#             }}
#             .info {{
#                 background: rgba(255, 255, 255, 0.2);
#                 padding: 15px;
#                 border-radius: 5px;
#                 margin: 10px 0;
#             }}
#             .endpoint {{
#                 background: rgba(0, 0, 0, 0.3);
#                 padding: 10px;
#                 margin: 10px 0;
#                 border-radius: 5px;
#                 font-family: monospace;
#             }}
#             a {{
#                 color: #FFD700;
#                 text-decoration: none;
#                 font-weight: bold;
#             }}
#             a:hover {{
#                 text-decoration: underline;
#             }}
#         </style>
#     </head>
#     <body>
#         <div class="container">
#             <h1>🚀 Python Data Processing API</h1>
#             <div class="info">
#                 <p><strong>Status:</strong> Running ✅</p>
#                 <p><strong>Uptime:</strong> {uptime}</p>
#                 <p><strong>Started:</strong> {start_time.isoformat()}</p>
#                 <p><strong>Current Time:</strong> {datetime.now().isoformat()}</p>
#             </div>
            
#             <h2>📚 Available Endpoints:</h2>
#             <div class="endpoint"><strong>GET</strong> / - This welcome page</div>
#             <div class="endpoint"><strong>GET</strong> /health - Health check</div>
#             <div class="endpoint"><strong>POST</strong> /process - Process data and calculate statistics</div>
#             <div class="endpoint"><strong>GET</strong> /fibonacci/{{n}} - Calculate Fibonacci number</div>
            
#             <h2>📖 Documentation:</h2>
#             <div class="info">
#                 <p>🔗 <a href="/docs">Interactive API Docs (Swagger UI)</a></p>
#                 <p>🔗 <a href="/redoc">Alternative API Docs (ReDoc)</a></p>
#             </div>
#         </div>
#     </body>
#     </html>
#     """
#     return {"message": "Hello, FastAPI!"}
#     return html_content

# @app.get("/health", response_model=HealthResponse)
# async def health_check():
#     """Health check endpoint"""
#     uptime = datetime.now() - start_time
#     logger.info("Health check requested")
#     print(typing.__file__)
#     print(f"sys is: {sys}")
#     print(f"user site packages are: {site.getusersitepackages()}")

#     return HealthResponse(
#         status="healthy",
#         uptime=str(uptime),
#         timestamp=datetime.now().isoformat(),
#         output= sys.path.__str__() + ", --- " + sys.argv.__str__()
#     )

# @app.post("/process", response_model=ProcessDataResponse)
# async def process_endpoint(request: ProcessDataRequest):
#     """
#     Process a list of numbers and return statistics
    
#     - **data**: List of numbers to process
    
#     Returns statistics (sum, average, max, min, count) and a Fibonacci sequence
#     """
#     logger.info(f"Process endpoint called with {len(request.data)} items")
#     return process_data(request.data)

# @app.get("/fibonacci/{n}", response_model=FibonacciResponse)
# async def fibonacci_endpoint(n: int):
#     """
#     Calculate the nth Fibonacci number
    
#     - **n**: The position in the Fibonacci sequence (must be >= 0)
#     """
#     if n < 0:
#         raise HTTPException(status_code=400, detail="n must be non-negative")
#     if n > 1000:
#         raise HTTPException(status_code=400, detail="n too large (max 1000)")
    
#     logger.info(f"Calculating Fibonacci({n})")
#     result = calculate_fibonacci(n)
    
#     return FibonacciResponse(
#         n=n,
#         result=result,
#         timestamp=datetime.now().isoformat()
#     )
@app.get("/users")

@app.on_event("startup")
async def startup_event():
    """Run on application startup"""
    logger.info("FastAPI application started!")
    logger.info(f"API Documentation available at: http://localhost:8000/docs")
    logger.info(f"Alternative docs available at: http://localhost:8000/redoc")
    
    # Initialize database tables
    try:
        from database import Base, engine
        from models import User, ProcessedData
        logger.info("Creating database tables if they don't exist...")
        Base.metadata.create_all(bind=engine)
        logger.info("✅ Database tables ready!")
    except Exception as e:
        logger.error(f"❌ Error initializing database: {e}")

@app.on_event("shutdown")
async def shutdown_event():
    """Run on application shutdown"""
    logger.info("FastAPI application shutting down...")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)