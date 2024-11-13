"""
routes.py
-------------
A resource class for retrieving energy data and calculating energy data averages.

Methods:
    get: Retrieves the latest energy data from Redis.
    get_average: Calculates and returns the average of recent energy data.
"""

from flask import jsonify, current_app
from flask_restful import Resource
import redis


class EnergyDataResource(Resource):
    """
    Retrieve the latest energy data from Redis.
    --------------
    Returns:
        - JSON response containing the latest energy data if available,
            or an error message if no data is found.
        - HTTP status 200 if data is available, or 404 if no data is available.
    """
    @staticmethod
    def get():
        energy_data= current_app.redis_cache.get_latest_energy_data()
        if energy_data:
            return jsonify({"status": "success", "data": energy_data}), 200
        else:
            return jsonify({"status": "error", "message": "No data available"}), 404

    @staticmethod
    def get_average():
        """
        Calculate and retrieve the average energy consumption from recent data in Redis.
        ----------
        Returns:
            - JSON response containing the average energy consumption if data is available,
              or an error message if no data is available for calculation.
            - HTTP status 200 if data is available, or 404 if no data is available.
        """
        energy_values = current_app.redis_cache.get_all_energy_data()
        if energy_values:
            average = sum(float(data['value']) for data in energy_values) / len(energy_values)
            return jsonify({'status': 'success', 'average_energy': average}), 200
        else:
            return jsonify({"status": "error", "message": "No data available for average calculation"}), 404

def configure_routes(app):
    """
    Register routes to the Flask application.
    -----------------
    Args:
        app (Flask): The Flask application instance to which routes are added.

    Adds:
        - '/energy' route for retrieving the latest energy data.
        - '/energy_data/average' route for retrieving the average energy data.
    """
    app.add_url_rule('/energy', view_func=EnergyDataResource.get, methods=['GET'])
    app.add_url_rule('/energy_data/average', view_func=EnergyDataResource.get_average, methods=['GET'])
