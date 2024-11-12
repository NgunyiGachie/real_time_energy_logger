"""
cache.py
----------
A class for interacting with Redis to cache and retrieve energy data. This class allows for setting,
retrieving, and pushing energy data entries to a Redis server, including functionality to keep only
the latest entries by limiting list length.

Attributes:
    host (str): The Redis server host (default is 'localhost').
    port (int): The Redis server port (default is 6379).
    _client (redis.StrictRedis): The Redis client instance.
"""

import json
import redis
from typing import List, Optional, Union

class RedisCache:
    def __init__(self, host='localhost', port=6379):
        """
        Initialize the RedisCache instance with Redis connection details.

        Args:
            host (str): The Redis server hostname or IP address.
            port (int): The Redis server port number.
        """
        self.host = host
        self.port = port
        self._client = None

    def get_client(self) -> redis.StrictRedis:
        """
        Establishes and returns the Redis client.

        Returns:
            redis.StrictRedis: An instance of the Redis client.
        """
        if self._client is None:
            self._client = redis.StrictRedis(host=self.host, port=self.port, decode_responses=True)
        return self._client

    def get_latest_energy_data(self) -> Optional[str]:
        """
        Retrieve the latest cached energy data from Redis.

        Returns:
            Optional[str]: The latest energy data as a string, or None if no data is available.
        """
        try:
            energy_data = self.get_client().get('latest_energy_data')
            return energy_data if energy_data else None
        except redis.ConnectionError as e:
            print(f"Redis connection error: {e}")
            return None

    def set_latest_energy_data(self, energy_data: Union[str, dict]) -> None:
        """
        Store the latest energy data in Redis. If the data is provided as a dictionary,
        it will be serialized to JSON format before storing.

        Args:
            energy_data (Union[str, dict]): The energy data to store, as a string or dictionary.
        """
        try:
            if isinstance(energy_data, dict):
                energy_data = json.dumps(energy_data)
            self.get_client().set('latest_energy_data', energy_data)
        except redis.ConnectionError as e:
            print(f"Redis connection error: {e}")

    def get_all_energy_data(self) -> List[dict]:
        """
        Retrieve all energy data entries stored in the Redis list.

        Returns:
            List[dict]: A list of dictionaries containing all stored energy data.
        """
        try:
            energy_data_list = self.get_client().lrange('energy_data_list', 0, -1)
            return [json.loads(data) for data in energy_data_list]
        except redis.ConnectionError as e:
            print(f"Redis connection error: {e}")
            return []

    def push_energy_data(self, energy_data: Union[str, dict], max_length: int = 100) -> None:
        """
        Add a new entry to the energy data list in Redis and limit the list length.
        If the list exceeds `max_length`, older entries are removed.

        Args:
            energy_data (Union[str, dict]): The energy data to store, as a string or dictionary.
            max_length (int): The maximum allowed list length (default is 100).
        """
        try:
            if isinstance(energy_data, dict):
                energy_data = json.dumps(energy_data)
            client = self.get_client()
            client.lpush('energy_data_list', energy_data)
            client.ltrim('energy_data_list', 0, max_length - 1)
        except redis.ConnectionError as e:
            print(f"Redis connection error: {e}")
