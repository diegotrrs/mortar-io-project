import unittest
from flask_testing import TestCase
from app import app  # Replace with your actual Flask app instance

# Test cases for the Add Report to City Endpoint
# Note: Because of time only test cases for the add a report endpoint are included, but ideally we should have a test case group for each endpoint
class TestAddReportToCity(TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        return app

    def test_it_should_add_report_to_city(self):
        """It should add a report sucessfully to a city if the data is correct"""
        data = {
                "temperature": 2,
                "condition": "Rainy",
                "timestamp": 1667983762005
        }
        response = self.client.post("/weather-api/cities/london/reports", json=data)
        data = response.get_json()
        self.assertEqual(response.status_code, 200)        
        self.assertEqual({"message": "Weather report added successfully for london"}, data)

        all_london_reports_response = self.client.get("/weather-api/cities/london/reports")
        data = all_london_reports_response.get_json()
        self.assertEqual(response.status_code, 200)        
        self.assertEqual([{'condition': 'Rainy', 'temperature': 2.0, 'timestamp': 1667983762005}], data)

    def test_it_should_validate_timestamp_is_missing(self):
        """It should return a 400 error if the timestamp is missing"""
        data = {
                "temperature": 2,
                "condition": "Rainy",                
        }
        response = self.client.post("/weather-api/cities/london/reports", json=data)
        data = response.get_json()
        self.assertEqual(response.status_code, 400)
        
        self.assertEqual("timestamp", data["errors"][0]["loc"][0])
        self.assertEqual("Field required", data["errors"][0]["msg"])
        self.assertEqual("missing", data["errors"][0]["type"])
    
    def test_it_should_validate_temperature_is_in_wrong_format(self):
        """It should return a 400 error if the temperature is in wrong format"""
        data = {
                "temperature": "This is not a valid format",
                "condition": "Rainy",
                "timestamp": 1667983762005
        }
        response = self.client.post("/weather-api/cities/london/reports", json=data)
        data = response.get_json()
        self.assertEqual(response.status_code, 400)
        
        self.assertEqual("temperature", data["errors"][0]["loc"][0])
        self.assertEqual("Input should be a valid number, unable to parse string as a number", data["errors"][0]["msg"])
        self.assertEqual("float_parsing", data["errors"][0]["type"])       

        
if __name__ == "__main__":
    unittest.main()




