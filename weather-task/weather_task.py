import os
import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("OPENWEATHER_API_KEY")

def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    return response.json()

cities = ["Sofia", "Melbourne", "Tokyo", "Los Angeles", "Cape Town"]

for city in cities:
    data = get_weather(city)
    if data.get("main"):
        print(f"Weather in {city}: {data['main']['temp']}°C, {data['weather'][0]['description']}")
    else:
        print(f"Could not fetch weather for {city}")
