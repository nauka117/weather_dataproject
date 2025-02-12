from src.data_loading.weather_requests import (
    HistoryWeatherRequestBase
)


def request_and_save(request: HistoryWeatherRequestBase):
    directories = {
        "HistoryWeatherRequestOWM": "OpenWeatherMap",
        "HistoryWeatherRequestVC": "VisualCrossing",
        "HistoryWeatherRequestMeteostat": "Meteostat",
        "HistoryWeatherRequestWeatherapi": "Weatherapi",
        "HistoryWeatherRequestWeatherbit": "Weatherbit"
    }


    response = request.query()

    cur_dir = directories[request.__class__.__name__]


    with open(f"src/data_loader/data/{cur_dir}/{request.startDateTime}.json", "w") as f:
        f.write(response.text)