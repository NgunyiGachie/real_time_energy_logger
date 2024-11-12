from confluent_kafka.admin import AdminClient, NewTopic

class Admin:
    def __init__(self, bootstrap_server):
        self.bootstrap_server = bootstrap_server
        self.admin = AdminClient({'bootstrap.servers': self.bootstrap_server})

    def topic_exists(self, topic):
        metadata = self.admin.list_topics(timeout=10)
        return topic in metadata.topics.keys()

    def create_topic(self, topic):
        if not self.topic_exists(topic):
            new_topic = NewTopic(topic, num_partitions=1, replication_factor=1)
            self.admin.create_topics([new_topic])
            print(f"Topic: {topic} has been created")