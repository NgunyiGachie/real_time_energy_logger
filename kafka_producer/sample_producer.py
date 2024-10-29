from confluent_kafka import Producer
from .admin import Admin

class ProducerClass:
    #initialization
    def __init__(self, bootstrap_server):
        self.bootstrap_server = bootstrap_server
        self.producer = Producer({'bootstrap.servers': self.bootstrap_server})

    def send_message(self, message):
        try:
            self.producer.produce(self.topic, message)
        except Exception as e:
            print(e)

    def commit(self):
        self.producer.flush()

if __name__ == '__main__':
    bootstrap_server = 'localhost:9092'
    topic = 'test-topic'
    a = Admin()
    p = ProducerClass()

    while True:
        try:
            message = input("Enter your message")
            p.send_message(message)
        except KeyboardInterrupt:
            pass
    p.commit()