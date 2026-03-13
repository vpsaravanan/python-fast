# config/redis_client.py
import redis
import os

redis_client = redis.Redis(
    host='host.docker.internal', #os.getenv('REDIS_HOST', '127.0.0.1'),
    port=int(os.getenv('REDIS_PORT', 6379)),
    decode_responses=True  # Returns strings instead of bytes
)

# Test connection
try:
    redis_client.ping()
    print("Connected to Redis!")
except redis.ConnectionError:
    print("Redis connection failed")