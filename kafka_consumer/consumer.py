"""
Kafka consumer for reading and processing events
"""
from Kafka import KafkaConsumer

"""To consume latest messages and autocommit offsets"""
consumer = KafkaConsumer('energy-report',
                        group_id = 'my-group',
                        bootstrap_servers=['localhost:9092'])
for message in consumer:
    print("%s:%d: key=%s value=%s" %(message.topic,
                                    message.partition,
                                    message.offset, message.key,
                                    message.value))