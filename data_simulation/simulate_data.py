"""
Simulate data
"""
import json
import random
import time
import kafka
from kafka import KafkaProducer

"""Configure kafka producer"""
producer = KafkaProducer(bootstrap_servers='localhost:9092')

"""function to generate random energy consumption data"""
def generate_data(sensor_id):
    return{
        "sensor_id": sensor_id,
        "timestamp": int(time.time()),
        "energy_consumption": round(random.uniform(100.0, 500.0), 2)
    }

def main():
    sensor_id = 1
    while True:
        energy_data = generate_data(sensor_id)
        producer.send('energy_consumption_topic', json.dumps(energy_data).encode('utf-8'))
        print(f"sent data: {energy_data}")
        time.sleep(10)

if __name__ == "__main__":
    main()