from pydantic import BaseModel


class CityWeatherReport(BaseModel):
    """Represents a weather report for a city"""

    temperature: int
    condition: str
    timestamp: int


class CityWeatherReportUpdateInformation(CityWeatherReport):
    """Represents a partial weather report for a city, used when updating a specific CityWeatherReport"""

    timestamp: int = None
