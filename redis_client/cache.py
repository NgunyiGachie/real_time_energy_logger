import json
import redis
from typing import List, Optional, Union

class RedisCache:
    def __init__(self, host= 'localhost', port= 6379):
        """
        Initialize the RedisCache instance with Redis connection details.
        """
        self.host = host
        self.port = port
        self._client = None

    def get_client(self):
        """
        Returns the Redis client
        """
        if self._client is None:
            self._client = redis.StrictRedis(host=self.host, port=self.port, decode_responses=True)
        return self._client

    def get_latest_energy_data(self) -> Optional[str]:
        """
        Get the latest cached energy data from Redis.
        Returns the latest energy data or None if no data is available.
        """
        try:
            energy_data = self.redis_client.get('latest_energy_data')
            if energy_data:
                return energy_data
            return None
        except redis.ConnectionError as e:
            print(f"Redis connection error: {e}")
            return None

    def set_latest_energy_data(self, energy_data: Union[str, dict]) -> None:
        """
        Store the latest energy data in Redis.
        The data will be converted to JSON format if it is a dictionary.
        """
        try:
            if isinstance(energy_data, dict):
                energy_data = json.dumps(energy_data)
            self.redis_client.set('latest_energy_data', energy_data)
        except redis.ConnectionError as e:
            print(f"Redis connection error: {e}")

    def get_all_energy_data(self) -> List[dict]:
        """
        Get all energy data stored in the Redis list.
        Returns a list of energy data dictionaries.
        """
        try:
            energy_data_list = self.redis_client.lrange('energy_data_list', 0, -1)
            return [json.loads(data) for data in energy_data_list]
        except redis.ConnectionError as e:
            print(f"Redis connection error: {e}")
            return []

    def push_energy_data(self, energy_data: Union[str, dict], max_length: int = 100) -> None:
        """
        Add energy data to a list in Redis, trimming it to a specified length.
        The data will be converted to JSON format if it's a dictionary.
        """
        try:
            if isinstance(energy_data, dict):
                energy_data = json.dumps(energy_data)
            self.redis_client.lpush('energy_data_list', energy_data)
            self.redis_client.ltrim('energy_data_list', 0, max_length - 1)
        except redis.ConnectionError as e:
            print(f"Redis connection error: {e}")
