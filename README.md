# Real Time Energy Logger with Confluent Kafka
A Flask-based API designed for caching, producing, and consuming real-time energy consumption data. This API integrates Redis for fast data access and Confluent Kafka (configured with Redpanda)for message streaming, allowing for efficient ingestion and processing of data in real time.
# Table of Contents
- Project Overview
- Features
- Prerequisites
- Installation
- Configuration
- Usage
- Kafka Producer and Consumer
- Future Improvements
# Project Overview
This API is designed to capture, cache, and process real-time energy consumption data. Redis provides high-speed access to the latest energy data, while Confluent Kafka (Integrated with Redpanda) facilitates the streaming of messages, enabling efficient data production and consumption.
# Features
- Real-Time Data Caching: Uses Redis to cache the latest energy data for fast retrieval.
- Message Streaming with Kafka: Integrates Confluent Kafka for scalable data ingestion and processing.
- Flexible Storage Options: Supports Redis for caching; extensible to PostgreSQL for persistent storage.
- Day-Specific Endpoints: Allows users to filter data by specific dates.
- Automatic Data Expiry: Limits Redis list size to maintain efficiency.
# Prerequisites
- Python 3.8+
- Redis installed and running
- Confluent Kafka setup with Redpanda for optimized data streaming
- Flask and required libraries (redis-py, confluent_kafka)
- Optional: PostgreSQL (for persistent data storage)
# Installation
1. Clone the repository:
    `git clone https://github.com/NgunyiGachie/real_time_energy_logger.git`
    `cd real_time_energy_logger`
2. Set up a virtual environment:
    `python3 -m venv venv`
    `source venv/bin/activate`
3. Install dependencies:
    `pip install -r requirements.txt`
4. Set up Redis: Ensure Redis is running on `localhost:6379` or update the configuration in `cache.py`.
5. Set up Kafka with Redpanda:
    - Install and start Redpanda, configured to work with Confluent Kafka on your system or connect to a hosted Confluent Kafka + Redpanda instance.
    - Configure the Kafka producer and consumer settings in kafka_config.py.
# Configuration
## Redis
Edit connection details in `cache.py`:
    - host: Redis server hostname (default: localhost)
    - port: Redis server port (default: 6379)

## Confluent Kafka with Redpanda
Configure the producer and consumer settings in kafka_config.py:

    - bootstrap.servers: Set this to your Redpanda broker(s), which are compatible with Kafka.
    - group.id: Consumer group ID.
    - auto.offset.reset: Determines the starting offset for consumers.
# Usage
# Running the API
Start the Flask app with:
    `python app.py`

Example Data Structure in Redis:

   json
   {
       "sensor_id": 1,
       "timestamp": 1636447621,
       "energy_consumption": 250.5
   }

# Kafka Producer and Consumer
This project uses Confluent Kafka with Redpanda as follows:
- **Kafka Producer**: Publishes energy data messages to a specified Kafka topic whenever new data is ingested. The producer is set up to serialize data as JSON.
- **Kafka Consumer**: Subscribes to the Kafka topic to consume energy data messages, which are then cached in Redis. The consumer runs continuously to capture real-time data.

# Future Improvements
- **Persistent Data Storage**: Add PostgreSQL support for long-term data retention.
- **Data Aggregation**: Implement daily, weekly, and monthly statistics aggregation.
- **API Security**: Introduce token-based authentication to secure endpoints.
