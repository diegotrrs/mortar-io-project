# 1. Description of the solution

The solution implements a Rest API using Flask. It makes use of the [Pydantic](https://docs.pydantic.dev/latest/) library to define the models and leverage the data validation that comes with it.

A flat folder structure was chosen in order to keep things simple.

## 1.1 Models

The models can be found in the ``src/models.py`` file. CityWeatherReport represents a weather report for a city. Because of time the following decisions were taken:

-  temperature is defined as a float, and the scale is not saved (e.g.: Celsius or Fahrenheit). Not range validation is performed for this field.

- condition is defined as a string that can contain anything. Ideally, the conditions should be defined as a enum.

- timestamp is defined as a integer.

```python
class CityWeatherReport(BaseModel):
    """Represents a weather report for a city"""

    temperature: float
    condition: str
    timestamp: int

```

By using Pydantic the type and presence of those fields is ensured. More details can be found below.


## 1.2 The app.py and weather_reports_manager.py files

The ``app.py`` file sets up the Flask app and it includes the routes. It formats the endpoint's response with the specific HTTP codes. It performs basic input validation (see ``ValidationError``) by instantiating the Pydantic's model.

In the other hand, ``weather_reports_manager.py`` deals with the weather reports in memory. It knows nothing about HTTP or Flask. The weather reports are defined as a ``Dictionary`` where each key is the city and each entry is a ``List`` of ``CityWeatherReport``.  For example if there was two entries for the city of London and one entry for Madrid the weather reports object would look like this:

```
{
  'london': [
    CityWeatherReport(temperature=10, condition='Cloudy', timestamp=1667983762000), CityWeatherReport(temperature=12, condition='Rainy', timestamp=1667983763000)
  ],
  'madrid': [
    CityWeatherReport(temperature=23, condition='Sunny', timestamp=11667983762100), 
  ]
}
```

This approach was favoured instead of a single list because the access would be quicker if the number of cities grows.

## 1.3 Exceptions

- ```CityNotFoundError``` is raised when an endpoint receives a city that does not exist. 
- ```ValidationError``` is raised when an endpoint receives a parameter in the wrong format (e.g.: timestamp as a alphabetic string) or when the parameter is missing at all.

## 1.4 Testing
Python's unittest is used for unit testing. There are two files that include tests:

- test_weather_reports_manager: Tests all of the functions for the ``WeatherReportsManager``. It doesn't include anything related to Flask or Http status codes. It's just business logic.

- test_app.py: Tests the Flask app's endpoints using the ```flask_testing``` package. It includes test cases for data in an incorrect format.

> In test_app.py, because of time only test cases for the add a report endpoint are included, but ideally we should have a test case group for each endpoint


# 2. How to install

The project uses [Poetry](https://python-poetry.org/) as for packing and dependency management. Therefore, you might need to install poetry first. Follow the instructions [here](https://python-poetry.org/docs/#installing-with-pipx) or run the following command

```bash
pipx install poetry
```

and then from the root folder of the project run:
```bash
poetry install
```

# 3. How to start the server

From the root folder run:
```bash
poetry run python src/app.py
```

# 4. How to test the API

The following are examples of CURL commands you can use to test each endpoint. Please change the values accordingly.

## 4.1 Add a weather report for a city (POST)

URL: ``/weather-api/cities/<string:city_id>/reports`` <br>
METHOD: ``POST`` <br>
EXAMPLE: 
```bash
curl --location 'http://127.0.0.1:5000/weather-api/cities/london/reports' \
--header 'Content-Type: application/json' \
--data '{
    "temperature": 2,
    "condition": "Rainy",
    "timestamp": 1667983762000
}'
```

## 4.2 Retrieve the latest weather report for a given city (GET)
URL: ``/weather-api/cities/<string:city_id>/reports/latest`` <br>
METHOD: ``GET`` <br>
EXAMPLE: 
```bash
curl --location 'http://127.0.0.1:5000/weather-api/cities/london/reports/latest'
```


## 4.3 Retrieve a summary of all ci?es currently in the system with their latest weather conditons (GET). 
URL: ``/weather-api/cities/summary`` <br>
METHOD: ``GET`` <br>
EXAMPLE: 
```bash
curl --location 'http://127.0.0.1:5000/weather-api/cities/summary'
```

## 4.4 Update the latest weather report for a specific city (PUT)
URL: ``/weather-api/cities/<string:city_id>/reports/latest`` <br>
METHOD: ``PUT`` <br>
EXAMPLE: 
```bash
curl --location --request PUT 'http://127.0.0.1:5000/weather-api/cities/london/reports/latest' \
--header 'Content-Type: application/json' \
--data '{
    "temperature": 20.5,
    "condition": "Sunny"
}'
```

## 4.5 Delete all weather reports for a specific city (DELETE)
URL: ``/weather-api/cities/<string:city_id>/reports`` <br>
METHOD: ``DELETE`` <br>
EXAMPLE: 
```bash
curl --location --request DELETE 'http://127.0.0.1:5000/weather-api/cities/london/reports'
```

## 4.6 Extra: Get all of the reports for a specific city (GET)
URL: ``/weather-api/cities/<string:city_id>/reports`` <br>
METHOD: ``GET`` <br>
EXAMPLE: 
```bash
curl --location 'http://127.0.0.1:5000/weather-api/cities/london/reports'
```

# 5. How to run the tests

From the root folder run:
```bash
poetry run python -m unittest discover -s src
```

In the ``test_weather_reports_manager.py`` file. The test cases are grouped by each of the WeatherReportsManager methods and they include "happy paths" as well as paths were Exceptions are thrown. The ``test_app.py`` file includes tests add report endpoint.


# 6. Improvements
- Extend the test cases for the flask app to test all of the endpoints.
- Define Conditions as an Enum and validate that the value specified is valid.
- The scale system for the temperature should be defined part of the system (e.g: Celsius).


# 7. Assumptions
In the description when it said "latest weather report" it was assumed that it was the report with the highest timestamp.