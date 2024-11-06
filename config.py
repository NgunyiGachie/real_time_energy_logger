from redis_cache import RedisCache

import os
from dashboard.app import app

"""Redis configuration"""
redis_host = os.getenv('REDIS_HOST', 'localhost')
redis_port = os.getenv('REDIS_PORT', 6379)
app.redis_cache = RedisCache(host=redis_host, port=redis_port)

"""Kafka configuration"""
kafka_topic = os.getenv('KAFKA_TOPIC', 'energy_data')
kafka_servers = os.getenv('KAFKA_SERVERS', 'localhost:9092')
