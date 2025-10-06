from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .main import main
from pydantic import BaseModel

app = FastAPI()


origins = [
    "http://localhost:5500",
    "http://127.0.0.1:5500",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class WeatherRequest(BaseModel):
    station: str = "KCDA"
    year: str = "2024"
    month: str = "12"
    day: str = "5"


@app.post("/api/weather")
def get_weather(request: WeatherRequest):
    result = main(
        station=request.station, year=request.year, month=request.month, day=request.day
    )
    return result
