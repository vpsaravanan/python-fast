from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
import time

# Example blocked IPs list
blocked_ips = ["192.168.1.100", "10.0.0.50"]

class CustomMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Example: Block specific IPs
        if request.client.host in blocked_ips:
            return Response("Blocked", status_code=403)
            
        # Example: Add request timing
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = str(process_time)
        
        return response