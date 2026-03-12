import redis
import json
import os

redis_client = redis.Redis(
    host=os.getenv('REDIS_HOST', 'localhost'),
    port=int(os.getenv('REDIS_PORT', 6379)),
    db=0,
    decode_responses=True
)

def get_from_cache(key: str):
    try:
        value = redis_client.get(key)
        if value:
            return json.loads(value)
    except Exception:
        pass
    return None

def set_to_cache(key: str, value, ttl: int = 300):
    try:
        redis_client.setex(key, ttl, json.dumps(value))
    except Exception:
        pass

def invalidate_cache(pattern: str):
    try:
        keys = redis_client.keys(pattern)
        if keys:
            redis_client.delete(*keys)
    except Exception:
        pass