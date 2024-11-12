"""
admin.py
---------
This module manages kafka topics using the `Admin` class. It handles
creation and deletion of topics.

Usage:
    Import `Admin` in other modules to create or delete kafka.
"""

from confluent_kafka.admin import AdminClient, NewTopic

class Admin:
    """
    A class for managing kafka topics using AdminClient.
    ---------
    Attributes:
        bootstrap_server (str): Address of the kafka broker.
    """
    def __init__(self, bootstrap_server):
        """
        Initializes the admin client.
        ---------
        Args:
            bootstrap_server (str): Kafka broker address.
        """
        self.bootstrap_server = bootstrap_server
        self.admin = AdminClient({'bootstrap.servers': self.bootstrap_server})

    def topic_exists(self, topic):
        """
        Checks if a topic exists.
        ---------
        Args:
            topic (str): The name of the topic.
        """
        metadata = self.admin.list_topics(timeout=10)
        return topic in metadata.topics.keys()

    def create_topic(self, topic):
        """
        Creates a kafka topic if it does not exist.
        ----------
        Args:
            topic (str): The name of the topic to create.
        """
        if not self.topic_exists(topic):
            new_topic = NewTopic(topic, num_partitions=1, replication_factor=1)
            self.admin.create_topics([new_topic])
            print(f"Topic: {topic} has been created")