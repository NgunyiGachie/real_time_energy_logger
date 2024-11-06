import json
import redis

class Rediscache:
    def __init__(self, host='localhost', port=6379):
        self.redis_client = redis.Redis(host=host, port=port)

    def get_latest_energy_data(self):
        """
        Get the latest cached energy data from Redis
        """
        try:
            energy_data = self.redis_client.get('latest_energy_data')
            return energy_data.decode('utf-8') if energy_data else None
        except redis.ConnectionError as e:
            print(f"Redis connection error: {e}")
            return None

    def set_latest_energy_data(self, energy_data):
        """
        Store the latest energy data in Redis
        """
        try:
            self.redis_client.set('latest_energy_data', json.dumps(energy_data))
        except redis.ConnectionError as e:
            print(f"Redis connection error: {e}")

    def get_all_energy_data(self):
        """
        Get all energy data from a Redis list
        """
        try:
            energy_data_list = self.redis_client.lrange('energy_data_list', 0, -1)
            return [json.loads(data) for data in energy_data_list]
        except redis.ConnectionError as e:
            print(f"Redis connection error: {e}")
            return []

    def push_energy_data(self, energy_data, max_length=100):
        """
        Add energy data to a list in Redis, trimming it to a specified length
        """
        try:
            self.redis_client.lpush('energy_data_list', json.dumps(energy_data))
            self.redis_client.ltrim('energy_data_list', 0, max_length -1)
        except redis.ConnectionError as e:
            print(f"Redis connection error: {e}")