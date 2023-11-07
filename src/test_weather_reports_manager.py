import unittest
from exceptions import CityNotFoundError
from models import CityWeatherReport, CityWeatherReportUpdateInformation
from weather_reports_manager import WeatherReportManager


# Test cases for the add_report_to_city method
class TestAddReportToCity(unittest.TestCase):
    weather_report_manager = WeatherReportManager()

    def test_it_should_add_a_report_to_a_city(self):
        """It should add a report to a city"""

        self.weather_report_manager.add_report_to_city("london", {"temperature": 9, "condition": "Cloudy", "timestamp": 1667983762000})
        reports = self.weather_report_manager.get_all_reports_for_city("london")
        self.assertEqual(
            reports,
            [{"temperature": 9, "condition": "Cloudy", "timestamp": 1667983762000}],
        )


# Test cases for the get_latest_report_for_city method
class TestGetLatestReportForCity(unittest.TestCase):
    weather_report_manager = WeatherReportManager()

    weather_report_manager.add_report_to_city("madrid", CityWeatherReport(temperature=19, condition="Sunny", timestamp=166798376_2005))
    weather_report_manager.add_report_to_city("london", CityWeatherReport(temperature=10, condition="Rainy", timestamp=1))
    weather_report_manager.add_report_to_city("madrid", CityWeatherReport(temperature=17, condition="Cloudy", timestamp=166798376_2010))
    weather_report_manager.add_report_to_city("madrid", CityWeatherReport(temperature=18, condition="Partly Cloudy", timestamp=166798376_2000))

    def test_it_should_return_latest_report_for_existing_city(self):
        """It should return the latest report for an existing city"""

        expected_latest = CityWeatherReport(temperature=17, condition="Cloudy", timestamp=166798376_2010)
        latest = self.weather_report_manager.get_latest_report_for_city("madrid")

        self.assertEqual(
            latest,
            expected_latest,
        )

    def test_it_should_throw_exception_for_not_existing_city(self):
        """It should throw an Exception if the city does not exist"""

        with self.assertRaises(CityNotFoundError):
            self.weather_report_manager.get_latest_report_for_city("paris")


# Test cases for the get_all_cites_reports_summary method
class TestGetAllCitiesSummary(unittest.TestCase):
    def test_it_should_return_summary_for_all_cities(self):
        """It should return the summary that includes the latest reports for all cities"""

        weather_report_manager = WeatherReportManager()

        latest_madrid = CityWeatherReport(temperature=17, condition="Cloudy", timestamp=166798376_2010)
        latest_london = CityWeatherReport(temperature=9, condition="Rainy", timestamp=166798376_2108)
        latest_lisbon = CityWeatherReport(temperature=19, condition="Clear", timestamp=166798376_2008)

        weather_report_manager.add_report_to_city("madrid", CityWeatherReport(temperature=19, condition="Sunny", timestamp=166798376_2005))
        weather_report_manager.add_report_to_city("london", CityWeatherReport(temperature=10, condition="Rainy", timestamp=166798376_2008))
        weather_report_manager.add_report_to_city("madrid", latest_madrid)
        weather_report_manager.add_report_to_city("madrid", CityWeatherReport(temperature=18, condition="Partly Cloudy", timestamp=166798376_2000))
        weather_report_manager.add_report_to_city("london", latest_london)
        weather_report_manager.add_report_to_city("lisbon", latest_lisbon)

        summary = weather_report_manager.get_all_cites_reports_summary()
        self.assertEqual(
            summary,
            {"madrid": latest_madrid, "london": latest_london, "lisbon": latest_lisbon},
        )


# Test cases for the update_city_latest_report method
class TestDeleteReportsForCityMethod(unittest.TestCase):
    weather_report_manager = WeatherReportManager()
    weather_report_manager.add_report_to_city("madrid", CityWeatherReport(temperature=19, condition="Sunny", timestamp=166798376_2005))
    weather_report_manager.add_report_to_city("madrid", CityWeatherReport(temperature=17, condition="Cloudy", timestamp=166798376_2010))
    weather_report_manager.add_report_to_city("madrid", CityWeatherReport(temperature=18, condition="Partly Cloudy", timestamp=166798376_2000))

    def test_it_should_update_the_info_for_the_latest_report(self):
        """It should update the attributes of the latest weather report for a specific country."""

        self.weather_report_manager.update_city_latest_report("madrid", CityWeatherReportUpdateInformation(temperature=17, condition="Sunny"))
        latest_after_update = self.weather_report_manager.get_latest_report_for_city("madrid")

        self.assertEqual(
            latest_after_update,
            CityWeatherReport(temperature=17, condition="Sunny", timestamp=166798376_2010),
        )

    def test_it_should_throw_exception_for_not_existing_city(self):
        """It should throw an Exception if the city does not exist"""

        with self.assertRaises(CityNotFoundError):
            self.weather_report_manager.update_city_latest_report("paris", CityWeatherReportUpdateInformation(temperature=17, condition="Sunny"))


# Test cases for the delete_reports_for_city method
class TestDeleteReportsForCityMethod(unittest.TestCase):
    weather_report_manager = WeatherReportManager()

    london_reports = [CityWeatherReport(temperature=10, condition="Rainy", timestamp=166798376_2008), CityWeatherReport(temperature=9, condition="Rainy", timestamp=166798376_2108)]

    lisbon_reports = [
        CityWeatherReport(temperature=19, condition="Clear", timestamp=166798376_2008),
    ]

    madrid_reports = [
        CityWeatherReport(temperature=19, condition="Sunny", timestamp=166798376_2005),
        CityWeatherReport(temperature=17, condition="Cloudy", timestamp=166798376_2010),
        CityWeatherReport(temperature=18, condition="Partly Cloudy", timestamp=166798376_2000),
    ]

    def test_it_should_delete_all_reports_for_specific_city(self):
        """It should delete all weather reports for the specified city"""
        self.weather_report_manager.add_report_to_city("madrid", self.madrid_reports[0])
        self.weather_report_manager.add_report_to_city("madrid", self.madrid_reports[1])
        self.weather_report_manager.add_report_to_city("madrid", self.madrid_reports[2])

        self.weather_report_manager.add_report_to_city("london", self.london_reports[0])
        self.weather_report_manager.add_report_to_city("london", self.london_reports[1])

        self.weather_report_manager.add_report_to_city("lisbon", self.lisbon_reports[0])

        self.weather_report_manager.delete_reports_for_city("madrid")

        reports = self.weather_report_manager.get_weather_reports()

        self.assertEqual(
            reports,
            {"london": self.london_reports, "lisbon": self.lisbon_reports},
        )

    def test_delete_weather_reports_until_all_deleted(self):
        """It should delete all of the reports in the system if the delete_reports_for_city method is called for all of the cities"""
        self.weather_report_manager.add_report_to_city("madrid", self.madrid_reports[0])
        self.weather_report_manager.add_report_to_city("madrid", self.madrid_reports[1])
        self.weather_report_manager.add_report_to_city("madrid", self.madrid_reports[2])

        self.weather_report_manager.add_report_to_city("london", self.london_reports[0])
        self.weather_report_manager.add_report_to_city("london", self.london_reports[1])

        self.weather_report_manager.add_report_to_city("lisbon", self.lisbon_reports[0])

        self.weather_report_manager.delete_reports_for_city("madrid")
        self.weather_report_manager.delete_reports_for_city("london")
        self.weather_report_manager.delete_reports_for_city("lisbon")

        reports = self.weather_report_manager.get_weather_reports()

        self.assertEqual(
            reports,
            {},
        )

    def test_it_should_throw_exception_for_not_existing_city(self):
        """It should throw an Exception if the city does not exist"""

        with self.assertRaises(CityNotFoundError):
            self.weather_report_manager.delete_reports_for_city("paris")
