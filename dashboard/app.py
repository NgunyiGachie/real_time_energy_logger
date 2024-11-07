import os
import sys
from flask import Flask

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from redis_client.cache import RedisCache
from routes import configure_routes
from kafka_consumer.consumer import ConsumerClass

app = Flask(__name__)

configure_routes(app)

redis_host = os.getenv('REDIS_HOST', 'localhost')
redis_port = os.getenv('REDIS_PORT', 6379)
app.redis_cache = RedisCache(host=redis_host, port=redis_port)

kafka_servers = "localhost:9092"
kafka_topic = "energy_data"

kafka_topic = os.getenv('KAFKA_TOPIC', kafka_topic)
kafka_servers = os.getenv('KAFKA_SERVERS', kafka_servers)

consume_thread = ConsumerClass(
    topic=kafka_topic,
    servers=kafka_servers,
    redis_client=app.redis_cache.get_client()
)
consume_thread.start()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5555, debug=True)
