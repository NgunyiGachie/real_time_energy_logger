from flask import Flask
from routes import configure_routes
from config import kafka_servers, kafka_topic
from kafka_consumer.consumer import ConsumerClass

app = Flask(__name__)

"""Routes initialization"""
configure_routes(app)

"""Start kafka consumer"""
consume_thread = ConsumerClass(
    topic=kafka_topic,
    servers=kafka_servers,
    redis_client=app.redis_client
)
consume_thread.start()

if __name__=='__main__':
    app.run(host='0.0.0.0', port=555, debug=True)