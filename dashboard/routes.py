from flask import jsonify, current_app
from flask_restful import Resource
import redis


class EnergyDataResource(Resource):
    """Retrieve the latest energy data from Redis"""
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
        Calculate and retrieve the average of the recent energy data
        """
        energy_values = current_app.redis_cache.get_all_energy()
        if energy_values:
            average = sum(float(data['value']) for data in energy_values) / len(energy_values)
            return jsonify({'status': 'success', 'average_energy': average}), 200
        else:
            return jsonify({"status": "error", "message": "No data available for average calculation"}), 404

def configure_routes(app):
    """
    Register routes to the Flask application
    """
    app.add_url_rule('/energy', view_func=EnergyDataResource.get, methods=['GET'])
    app.add_url_rule('/energy_data/average', view_func=EnergyDataResource.get_average, methods=['GET'])
