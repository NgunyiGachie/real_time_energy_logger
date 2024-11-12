"""
Simulate data
"""
import json
import random
import time
from confluent_kafka import Producer

"""Configure kafka producer"""
p = Producer({'bootstrap.servers': 'localhost:19092'})

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
        p.produce('energy_consumption_topic', json.dumps(energy_data).encode('utf-8'))
        p.flush()
        print(f"sent data: {energy_data}")
        time.sleep(10)

if __name__ == "__main__":
    main()