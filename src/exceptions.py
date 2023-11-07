class CityNotFoundError(Exception):
    """Exception raised for errors in the specified city id does not exist."""

    def __init__(self, city_id: str):
        self.message = f"City {city_id} does not exist."
        super().__init__(self.message)
