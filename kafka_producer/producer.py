from confluent_kafka import Producer
from admin import Admin

class ProducerClass:
    #initializationc
    def __init__(self, bootstrap_server, topic):
        self.bootstrap_server = bootstrap_server
        self.topic = topic
        self.producer = Producer({'bootstrap.servers': self.bootstrap_server})

    def send_message(self, message):
        try:
            self.producer.produce(self.topic, message)
        except Exception as e:
            print(e)

    def commit(self):
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