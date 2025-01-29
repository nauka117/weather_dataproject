from pydantic import ValidationError

from settings import Settings



try:
    settings = Settings()
    print(settings)
except ValidationError as err:
    print(f"Error loading settings from .env file: {err}")