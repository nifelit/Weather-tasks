import os
import requests
import tkinter as tk
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("OPENWEATHER_API_KEY")

def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    return response.json()

def show_weather():
    city = city_entry.get()
    data = get_weather(city)
    if data.get("main"):
        result_label.config(
            text=f"{city}: {data['main']['temp']}°C, {data['weather'][0]['description']}"
        )
    else:
        result_label.config(text="Could not fetch weather")

root = tk.Tk()
root.title("Weather App")

tk.Label(root, text="Enter city:").pack()
city_entry = tk.Entry(root)
city_entry.pack()

tk.Button(root, text="Get Weather", command=show_weather).pack()
result_label = tk.Label(root, text="")
result_label.pack()

root.mainloop()
