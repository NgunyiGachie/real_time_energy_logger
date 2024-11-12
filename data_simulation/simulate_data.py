"""
Simulate_data.py
------------------
This script generates and sends simulated energy consumption data to the kafka topic
at regular intervals. The data includes sensor ID, timestamp, and random energy usage.

Usage:
    Run `python simulate_date.py` to start sending data to kafka.
"""

import json
import random
import time
from confluent_kafka import Producer

#Configure kafka producer
p = Producer({'bootstrap.servers': 'localhost:19092'})

def generate_data(sensor_id):
    """
    Generates a dictionary with random energy consumption data.
    -----------
    Args:
        sensor_id (int): The ID of the sensor.
    Returns:
        dict: A dictionary with sensor_id, timestamp, and energy consumption.
    """
    return{
        "sensor_id": sensor_id,
        "timestamp": int(time.time()),
        "energy_consumption": round(random.uniform(100.0, 500.0), 2)
    }

def main():
    """
    Main function that continously sends generated energy data to Kafka.
    """
    sensor_id = 1
    while True:
        energy_data = generate_data(sensor_id)
        p.produce('energy_consumption_topic', json.dumps(energy_data).encode('utf-8'))
        p.flush()
        print(f"sent data: {energy_data}")
        time.sleep(10)

if __name__ == "__main__":
    main()