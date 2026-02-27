import redis
import json
import os

redis_client = redis.Redis(
    host=os.getenv('REDIS_HOST', 'localhost'),
    port=6379,
    db=0,
    decode_responses=True
)

def get_from_cache(key: str):
    """Получить данные из кэша по ключу"""
    value = redis_client.get(key)
    if value:
        return json.loads(value)
    return None

def set_to_cache(key: str, value, ttl: int = 300):
    """Сохранить данные в кэше с заданным временем жизни (TTL)"""
    redis_client.setex(key, ttl, json.dumps(value))
    return value

def invalidate_cache(pattern: str):
    """Удалить все ключи, соответствующие шаблону (например, 'product:*')"""
    keys = redis_client.keys(pattern)
    if keys:
        redis_client.delete(*keys)
        return True
    return False