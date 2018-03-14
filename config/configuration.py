import os

def get_redis_host():
    return os.getenv('REDIS_HOST', '0.0.0.0')

def get_redis_port():
    return os.getenv('REDIS_PORT', '6379')

def get_duckling_host():
    return os.getenv('DUCKLING_HOST', 'http://0.0.0.0')

def get_duckling_port():
    return os.getenv('DUCKLING_HOST', '8000')
