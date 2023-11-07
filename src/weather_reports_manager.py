from typing import List, Dict
from exceptions import CityNotFoundError
from models import CityWeatherReport, CityWeatherReportUpdateInformation

WeatherReports = Dict[str, List[CityWeatherReport]]


class WeatherReportManager:

    """Manages weather reports for different cities. It allows you to add, retrieve, update, and delete weather reports for specific cities,
    as well as retrieve summaries of the latest weather reports for all cities stored in its memory.
    """

    def __init__(self):
        self.__weather_reports: WeatherReports = {}  # The weather reports in memory

    def get_weather_reports(self):
        return self.__weather_reports

    def __find_latest_report_for_city(self, city_id: str):
        reports_for_city = self.__weather_reports[city_id]
        return max(reports_for_city, key=lambda report: report.timestamp)

    def get_all_reports_for_city(self, city_id: str):
        if city_id in self.__weather_reports:
            return self.__weather_reports[city_id]
        else:
            raise CityNotFoundError(city_id)

    def add_report_to_city(self, city_id: str, report: CityWeatherReport):
        if city_id not in self.__weather_reports:
            self.__weather_reports[city_id] = []

        self.__weather_reports[city_id].append(report)

    def get_latest_report_for_city(self, city_id: str) -> CityWeatherReport:
        if city_id in self.__weather_reports:
            return self.__find_latest_report_for_city(city_id)
        else:
            raise CityNotFoundError(city_id)

    def get_all_cites_reports_summary(self):
        summary = {}
        for city in self.__weather_reports:
            latest_report = self.__find_latest_report_for_city(city)
            summary[city] = latest_report
        return summary

    def update_city_latest_report(self, city_id: str, new_latest_info: CityWeatherReportUpdateInformation):
        if city_id in self.__weather_reports:
            latest_report = self.__find_latest_report_for_city(city_id)
            latest_report.temperature = new_latest_info.temperature
            latest_report.condition = new_latest_info.condition
        else:
            raise CityNotFoundError(city_id)

    def delete_reports_for_city(self, city_id: str):
        if city_id in self.__weather_reports:
            del self.__weather_reports[city_id]
        else:
            raise CityNotFoundError(city_id)
