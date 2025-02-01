from abc import (
    ABC,
    abstractmethod
)

import datetime as dt

import re

import requests

from src.data_loader.settings import Settings
settings = Settings()


class HistoryWeatherRequestBase(ABC):
    def __init__(self):
        if self.__class__ == HistoryWeatherRequestBase:
            raise TypeError("WeatherQueryBase is an abstract class and cannot be instantiated directly.")
        self.base_url = None
        self.api_key = None
        self.location = {
            "latitude": None,
            "longitude": None,
            "location_name": None
        }
        self.startDateTime = {
            "ISO 8601": None,
            "unix": None
        }
        self.endDateTime = {
            "ISO 8601": None,
            "unix": None
        }

    def set_location_city(self, city_name: str):
        base_url = "https://nominatim.openstreetmap.org/search"
        params = {
            "q": city_name,
            "format": "json",
            "addressdetails": 0,
            "limit": 1
        }
        headers = {
            "User-Agent": settings.GC_API.user_agent
        }

        response = requests.get(base_url, params=params, headers=headers)
        if response.status_code == 200:
            results = response.json()
            if results:
                self.location["latitude"] = results[0]["lat"]
                self.location["longitude"] = results[0]["lon"]
                self.location["location_name"] = city_name
            else:
                print(f"No results found for city: {city_name}")
                return
        else:
            print(f"Error: {response.status_code}")
            return

    def set_location_coordinates(self, latitude: float, longitude: float):
        self.location = [latitude, longitude]
        base_url = "https://nominatim.openstreetmap.org/reverse"
        params = {
            "lat": latitude,
            "lon": longitude,
            "format": "json"
        }
        headers = {
            "User-Agent": settings.GC_API.user_agent
        }

        response = requests.get(base_url, params=params, headers=headers)
        if response.status_code == 200:
            results = response.json()
            if results:
                self.location["latitude"] = latitude
                self.location["longitude"] = longitude
                self.location["location_name"] = results["display_name"]
            else:
                print(f"No results found for coordinates: {latitude}, {longitude}")
                return
        else:
            print(f"Error: {response.status_code}")
            return

    def set_start_datetime(self, start_datetime: str):
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}", start_datetime):
            raise ValueError("startDateTime must be in the format YYYY-MM-DDTHH:MM:SS")

        date_time = dt.datetime.strptime(start_datetime, "%Y-%m-%dT%H:%M:%S")

        self.startDateTime["ISO 8601"] = date_time.isoformat()
        self.startDateTime["unix"] = int(date_time.timestamp())

    def set_end_datetime(self, end_datetime: str):
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}", end_datetime):
            raise ValueError("endDateTime must be in the format YYYY-MM-DDTHH:MM:SS")

        date_time = dt.datetime.strptime(end_datetime, "%Y-%m-%dT%H:%M:%S")

        self.endDateTime["ISO 8601"] = date_time.isoformat()
        self.endDateTime["unix"] = int(date_time.timestamp())

    @abstractmethod
    def get_query_params(self):
        pass

    @abstractmethod
    def get_headers(self):
        pass

    def query(self):
        if not all([self.base_url, self.api_key, self.location, self.startDateTime, self.endDateTime]):
            raise ValueError("All fields must be set before querying.")

        params = self.get_query_params()
        headers = self.get_headers()

        response = requests.get(self.base_url, params=params, headers=headers)
        return response.json()


class HistoryWeatherRequestOWM(HistoryWeatherRequestBase):
    def __init__(self):
        super().__init__()
        self.base_url = "https://history.openweathermap.org/data/2.5/history/city"
        self.api_key = settings.OWM_API.key

    def get_query_params(self):
        return {
            "lat": self.location["latitude"],
            "lon": self.location["longitude"],
            "type": "hour",
            "appid": self.api_key,
            "start": self.startDateTime["unix"],
            "end": self.endDateTime["unix"]
        }

    def get_headers(self):
        return {}


class HistoryWeatherRequestVC(HistoryWeatherRequestBase):
    def __init__(self):
        super().__init__()
        self.base_url = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/weatherdata/history"
        self.api_key = settings.VC_API.key

    def get_query_params(self):
        return {
            "location": f"{self.location['latitude']},{self.location['longitude']}",
            "aggregateHours": 1,
            "unitGroup": "metric",
            "key": self.api_key,
            "startDateTime": self.startDateTime["ISO 8601"],
            "endDateTime": self.endDateTime["ISO 8601"],
            "contentType": "json"
        }

    def get_headers(self):
        return {}

class HistoryWeatherRequestMeteostat(HistoryWeatherRequestBase):
    def __init__(self):
        super().__init__()
        self.base_url = "https://meteostat.p.rapidapi.com/point/hourly"
        self.api_key = settings.METEOSTAT_API.key

    def get_query_params(self):
        return {
            "lat": self.location['latitude'],
            "lon": self.location['longitude'],
            "start": self.startDateTime["ISO 8601"],
            "end": self.endDateTime["ISO 8601"]
        }

    def get_headers(self):
        return {
            "x-rapidapi-key": self.api_key,
            "x-rapidapi-host": "meteostat.p.rapidapi.com"
        }

class HistoryWeatherRequestWeatherapi(HistoryWeatherRequestBase):
    def __init__(self):
        super().__init__()
        self.base_url = "http://api.weatherapi.com/v1/history.json"
        self.api_key = settings.WEATHERAPI_API.key

    def get_query_params(self):
        return {
            "key": self.api_key,
            "q": f"{self.location['latitude']},{self.location['longitude']}",
            "dt": self.startDateTime["YYYY-MM-DD"],
            "end_dt": self.endDateTime["YYYY-MM-DD"]
        }

    def get_headers(self):
        return {}
