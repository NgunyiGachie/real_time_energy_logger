"""
producer.py
------------
This module sets up kafka producer that sends message to a specified kafka topic.
It includes a class `ProducerClass` for creating and managing the producer instance,
and an `Admin` class for topic creation and deletion.

usage:
    Run `python producer.py` to start the producer. It will prompt for input messages
    and send them to a specified kafka topic.
"""

from confluent_kafka import Producer
from admin import Admin

class ProducerClass:
    """
    A class for managing kafka producer and sending messages to a topic.
    -------
    Attributes:
        bootstrap_server (str): Address of the kafka broker.
        topic (str): Topic to which the messages will be sent.
    """
    def __init__(self, bootstrap_server, topic):
        """
        Initializes the producer with the specified kafka broker and topic.
        ------
        args:
            bootstrap_server (str): Kafka broker address.
            topic (str): Topic to send messages to.
        """
        self.bootstrap_server = bootstrap_server
        self.topic = topic
        self.producer = Producer({'bootstrap.servers': self.bootstrap_server})

    def send_message(self, message):
        """
        Sends a message to a specified kafka topic.
        -----
        Args:
            message (str): The message to send
        """
        try:
            self.producer.produce(self.topic, message)
        except Exception as e:
            print(e)

    def commit(self):
        """
        Waits for all messages in the producer to be delivered.
        """
        self.producer.flush()

if __name__ == '__main__':
    bootstrap_server = 'localhost:19092'
    topic = 'energy-topic'
    a = Admin(bootstrap_server)
    a.create_topic(topic)
    p = ProducerClass(bootstrap_server, topic)

    try:
        while True:
            message = input("Enter your message: ")
            if message.lower() == 'exit':
                print("Exiting producer...")
                break
            p.send_message(message)
    except KeyboardInterrupt:
            print("\nProducer interrupted")
    p.commit()