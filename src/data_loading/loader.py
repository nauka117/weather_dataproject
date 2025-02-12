from src.data_loading.weather_requests import (
    HistoryWeatherRequestBase
)

import os
from pathlib import Path

import json


def request_and_save(request: HistoryWeatherRequestBase):
    directories = {
        "HistoryWeatherRequestOWM": "OpenWeatherMap",
        "HistoryWeatherRequestVC": "VisualCrossing",
        "HistoryWeatherRequestMeteostat": "Meteostat",
        "HistoryWeatherRequestWeatherapi": "Weatherapi",
        "HistoryWeatherRequestWeatherbit": "Weatherbit"
    }


    response = request.query()

    project_root = Path(__file__).parent.parent.parent
    cur_dir = directories[request.__class__.__name__]

    save_dir = project_root / "data" / "raw" / cur_dir
    os.makedirs(save_dir, exist_ok=True)

    file_name = f"{request.startDateTime['unix']}.json"
    file_path = save_dir / file_name

    with open(file_path, "w") as f:
        json.dump(response, f, indent=4)