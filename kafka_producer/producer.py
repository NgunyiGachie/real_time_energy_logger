"""
Kafka producer for writing events to Kafka cluster
"""

from kafka import KafkaProducer
from kafka.errors import KafkaError
import logging as log

log.basicConfig(level=log.INFO)

producer = KafkaProducer(bootstrap_servers=['localhost:9092'])
future = producer.send('energy-data', b'raw_bytes')

"""
Block for synchronous sends
"""
try:
    record_metadata = future.get(timeout=10)
except KafkaError as e:
    """Handle producer request failure"""
    log.error("Failed to send message to Kafka: %s", e)
else:
    """Successful result returns assigned partition and offset"""
    log.info(f"Message sent to topic: {record_metadata.topic}")
    log.info(f"Message partition: {record_metadata.partition}")
    log.info(f"Message offset: {record_metadata.offset}")

producer.close()