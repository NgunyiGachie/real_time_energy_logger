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
redis_cache = RedisCache(host=redis_host, port=redis_port)

bootstrap_server = os.getenv('KAFKA_SERVERS', 'localhost:9092')
group_id = os.getenv('KAFKA_GROUP_ID', 'my-group-id')
topic = os.getenv('KAFKA_TOPIC', 'energy_data')

consume_thread = ConsumerClass(
    bootstrap_server=bootstrap_server,
    group_id=group_id,
    topic=topic,
    redis_cache=redis_cache
)
consume_thread.start()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5555, debug=True)
