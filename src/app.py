from flask import Flask, request, jsonify
from pydantic import ValidationError
from models import CityWeatherReport, CityWeatherReportUpdateInformation
from weather_reports_manager import CityNotFoundError, WeatherReportManager

app = Flask(__name__)

weather_report_manager = WeatherReportManager()


@app.route("/weather-api/cities/<string:city_id>/reports", methods=["GET"])
def get_all_reports_for_city(city_id: str):
    """
    Return all of the reports for a city
    """
    try:
        reports = weather_report_manager.get_all_reports_for_city(city_id)
        return jsonify([r.__dict__ for r in reports])

    except CityNotFoundError as e:
        return jsonify({"message": str(e)}), 404


@app.route("/weather-api/cities/<string:city_id>/reports", methods=["POST"])
def add_weather_report_to_city(city_id: str):
    """
    Add a weather report for a city
    """
    try:
        data = request.get_json()
        report = CityWeatherReport(**data)
        weather_report_manager.add_report_to_city(city_id, report)

        return jsonify({"message": f"Weather report added successfully for {city_id}"})

    except ValidationError as e:
        return jsonify({"errors": e.errors()}), 400


@app.route("/weather-api/cities/<string:city_id>/reports/latest", methods=["GET"])
def get_latest_weather_report(city_id: str):
    """
    Retrieve the latest weather report for a given city
    """
    try:
        latest_report = weather_report_manager.get_latest_report_for_city(city_id)
        return jsonify(latest_report.__dict__)

    except CityNotFoundError as e:
        return jsonify({"message": str(e)}), 404


@app.route("/weather-api/cities/summary", methods=["GET"])
def get_all_weather_reports():
    """
    Retrieve a summary of all cities currently in the system with their latest weather conditions
    """
    summary = weather_report_manager.get_all_cites_reports_summary()
    return {city: report.__dict__ for city, report in summary.items()}


@app.route("/weather-api/cities/<string:city_id>/reports/latest", methods=["PUT"])
def update_latest_weather_report(city_id: str):
    """
    Update the latest weather report for a specific city
    """
    data = request.get_json()
    try:
        report_update_info = CityWeatherReportUpdateInformation(**data)
        weather_report_manager.update_city_latest_report(city_id, report_update_info)
        return jsonify({"message": f"Latest weather report for {city_id} updated successfully"})

    except ValidationError as e:
        return jsonify({"errors": e.errors()}), 400

    except CityNotFoundError as e:
        return jsonify({"message": str(e)}), 404


@app.route("/weather-api/cities/<string:city_id>/reports", methods=["DELETE"])
def delete_weather_reports(city_id: str):
    """
    Delete all weather reports for a specific city
    """
    try:
        weather_report_manager.delete_reports_for_city(city_id)
        return jsonify({"message": f"All weather reports deleted for {city_id}"})

    except CityNotFoundError as e:
        return jsonify({"message": str(e)}), 404


if __name__ == "__main__":
    app.run()
