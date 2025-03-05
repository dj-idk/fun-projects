import redis
import os
import httpx
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with frontend URL if needed, e.g., ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

API_KEY = os.getenv("API_KEY")

redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

@app.get("/weather/{city}")
async def get_weather(city: str, country: str = None):
    if not API_KEY:
        return {"error": "API_KEY is missing. Set it in environment variables."}

    redis_key = f"weather_{city}_{country or 'unknown'}"

    cached_data = redis_client.get(redis_key)
    if cached_data:
        return {"city": city, "cached": True, "data": cached_data}

    async with httpx.AsyncClient() as client:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city},{country or ''}&appid={API_KEY}"
        response = await client.get(url)

    if response.status_code != 200:
        return {"error": "Failed to fetch weather data", "status_code": response.status_code}

    weather_data = response.text

    redis_client.setex(redis_key, 3600 * 3, weather_data)

    return {"city": city, "cached": False, "data": weather_data}


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
