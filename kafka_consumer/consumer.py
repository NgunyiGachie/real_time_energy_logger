"""
consumer.py
-------------
 A threaded Kafka consumer class that consumes messages from a specified Kafka topic
and optionally stores the latest message in a Redis cache.

Attributes:
    bootstrap_server (str): The Kafka bootstrap server address.
    group_id (str): The consumer group ID for Kafka.
    topic (str): The Kafka topic to subscribe to for consuming messages.
    redis_cache (Optional[RedisCache]): An optional RedisCache instance for caching messages.
    consumer (Consumer): The Kafka consumer instance for polling messages.
"""

import threading
import json
from confluent_kafka import Consumer

class ConsumerClass(threading.Thread):
    def __init__(self, bootstrap_server, group_id, topic, redis_cache=None):
        """
        Initialize Kafka consumer class and thread.
        ---------------
        Args:
            bootstrap_server (str): Kafka server address (e.g., 'localhost:9092').
            group_id (str): Kafka consumer group ID.
            topic (str): Kafka topic to consume messages from.
            redis_cache (Optional[RedisCache]): RedisCache instance for caching messages (optional).
        """
        threading.Thread.__init__(self)
        self.bootstrap_server = bootstrap_server
        self.group_id = group_id
        self.topic = topic
        self.redis_cache = redis_cache
        self.consumer = Consumer({"bootstrap.servers": self.bootstrap_server, "group.id": self.group_id})

    def consume_messages(self):
        """
        Start consuming messages from the Kafka topic and process each message.

        If a Redis cache is provided, stores the latest consumed message in Redis.
        Prints each consumed message to the console.

        Raises:
            KeyboardInterrupt: Allows graceful shutdown if interrupted manually.
        """
        self.consumer.subscribe([self.topic])
        try:
            while True:
                msg = self.consumer.poll(1)
                if msg is None:
                    continue
                if msg.error():
                    print(f"Error while consuming message: {msg.error()}")
                else:
                    message_value = msg.value().decode('utf-8')
                    try:
                        message_data = json.loads(message_value)
                        print(f"Message consumed: {message_data}")
                        if self.redis_cache:
                            self.redis_cache.set_latest_energy_data(msg.value())
                    except json.JSONDecodeError:
                        print(f"Error decoding JSON: {message_value}")
        except KeyboardInterrupt:
            pass
        finally:
            self.consumer.close()

    def run(self):
        """
        Override the `run` method of the threading.Thread class.

        Starts the message consumption process in a separate thread, calling `consume_messages`.
        """
        self.consume_messages()