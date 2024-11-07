import threading
from confluent_kafka import Consumer

class ConsumerClass(threading.Thread):
    def __init__(self, bootstrap_server, group_id, topic, redis_cache=None):
        """
        Initialize Kafka consumer class and thread.
        """
        threading.Thread.__init__(self)
        self.bootstrap_server = bootstrap_server
        self.group_id = group_id
        self.topic = topic
        self.redis_cache = redis_cache
        self.consumer = Consumer({"bootstrap.servers": self.bootstrap_server, "group.id": self.group_id})

    def consume_messages(self):
        """
        Start consuming messages from the Kafka topic.
        """
        self.consumer.subscribe([self.topic])
        try:
            while True:
                msg = self.consumer.poll(1, 0)
                if msg is None:
                    continue
                if msg.error():
                    print(f"Error while consuming message: {msg.error()}")
                print(f"Message consumed: {msg.value()}")
                if self.redis_cache:
                    self.redis_cache.set_latest_energy_data(msg.value())
        except KeyboardInterrupt:
            pass
        finally:
            self.consumer.close()

    def run(self):
        """
        Override the run method to start consuming messages in the thread.
        """
        self.consume_messages()