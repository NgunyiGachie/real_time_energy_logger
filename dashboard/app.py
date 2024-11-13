"""
app.py
-----------------------

This script initializes and runs a Flask application, configures routes, sets up Redis caching, and starts a Kafka consumer thread to asynchronously consume messages and cache the latest energy data.

Modules:
    - os: Provides a way of using operating system dependent functionality.
    - sys: Provides access to some variables used or maintained by the interpreter.
    - flask.Flask: Creates a Flask application instance.
    - redis_client.cache.RedisCache: Redis cache client class to store and retrieve data.
    - routes.configure_routes: Function to set up routes for the Flask application.
    - kafka_consumer.consumer.ConsumerClass: Kafka consumer class to consume messages in a thread.

Environment Variables:
    - REDIS_HOST (default='localhost'): The host address of the Redis server.
    - REDIS_PORT (default=6379): The port number of the Redis server.
    - KAFKA_SERVERS (default='localhost:9092'): The Kafka bootstrap server address.
    - KAFKA_GROUP_ID (default='my-group-id'): The consumer group ID for Kafka.
    - KAFKA_TOPIC (default='energy_consumption_topic'): The Kafka topic to consume.

Attributes:
    app (Flask): The Flask application instance.
    redis_cache (RedisCache): Redis cache client instance.
    consume_thread (ConsumerClass): Kafka consumer thread instance.

Usage:
    To run this application, run `python app.py`.
"""

import os
import sys
from flask import Flask

# Add the project's root directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from redis_client.cache import RedisCache
from routes import configure_routes
from kafka_consumer.consumer import ConsumerClass

# Initialize Flask application
app = Flask(__name__)

# Configure routes for the application
configure_routes(app)

# Set up Redis cache connection using environment variables, with defaults
redis_host = os.getenv('REDIS_HOST', 'localhost')
redis_port = os.getenv('REDIS_PORT', 6379)
redis_cache = RedisCache(host=redis_host, port=redis_port)
app.redis_cache = redis_cache

# Configure Kafka consumer settings from environment variables, with defaults
bootstrap_server = os.getenv('KAFKA_SERVERS', 'localhost:9092')
group_id = os.getenv('KAFKA_GROUP_ID', 'my-group-id')
topic = os.getenv('KAFKA_TOPIC', 'energy_consumption_topic')

# Create and start a Kafka consumer thread
consume_thread = ConsumerClass(
    bootstrap_server=bootstrap_server,
    group_id=group_id,
    topic=topic,
    redis_cache=redis_cache
)
consume_thread.start()

# Run the Flask application if this script is the main entry point
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5555, debug=True)
