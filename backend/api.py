from fastapi import FastAPI
from .main import main
from pydantic import BaseModel

app = FastAPI()

class WeatherRequest(BaseModel):
    station: str = "KCDA"
    year: str = "2024"
    month: str = "12"
    day: str = "5"

@app.post("/api/weather")
def get_weather(request: WeatherRequest):
    result = main(
        station=request.station,
        year=request.year,
        month=request.month,
        day=request.day
    )

    return result