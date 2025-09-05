import os
import redis
from fastapi import FastAPI, HTTPException
from schemas.key_value import KeyValueSchema, FetchKeySchema

app = FastAPI()

# --- Redis Connection ---
try:
    redis_client = redis.Redis(
        host=os.getenv("REDIS_HOST", "localhost"),
        port=os.getenv("REDIS_PORT", 6379),
        db=0,
        decode_responses=True # UTF-8
    )
    redis_client.ping()
    print("✅ Successfully connected to Redis!")
except redis.exceptions.ConnectionError as e:
    print(f"🔥 Failed to connect to Redis: {e}")
    redis_client = None 

@app.get("/status")
def get_status():
    if redis_client is None:
        raise HTTPException(status_code=503, detail="Redis connection not available")
    return {"status": "ok", "redis_connected": True}

@app.post("/items/")
def set_item(item: KeyValueSchema):
    if redis_client is None:
        raise HTTPException(status_code=503, detail="Redis connection not available")
    redis_client.set(item.key, item.value)
    return {"message": "success", "key": item.key, "value": item.value}

@app.get("/items/")
def get_item(key: FetchKeySchema):
    if redis_client is None:
        raise HTTPException(status_code=503, detail="Redis connection not available")

    value = redis_client.get(key.key)
    if value is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"key": key, "value": value}


# this is a syntax error