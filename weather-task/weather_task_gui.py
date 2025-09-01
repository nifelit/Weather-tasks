import requests
import statistics
import tkinter as tk
from tkinter import messagebox

API_KEY = "e04374202b1859b58802c8cdf1c58901" 
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
UNITS = "metric"
CITIES = ["Sofia,BG", "Melbourne,AU", "Tokyo,JP", "Los Angeles,US", "Cape Town,ZA"]


def get_weather(city):
    params = {"q": city, "appid": API_KEY, "units": UNITS}
    try:
        response = requests.get(BASE_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        temp = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        description = data["weather"][0]["description"]
        main_cond = data["weather"][0]["main"]
        if "rain" in main_cond.lower() or "snow" in main_cond.lower():
            condition = "Rain/Snow"
        elif "cloud" in main_cond.lower():
            condition = "Cloudy"
        else:
            condition = "Clear/Sunny"
        return {"city": city, "temp": temp, "humidity": humidity, "description": description, "condition": condition}
    except requests.RequestException as e:
        messagebox.showerror("Error", f"{city}: {e}")
        return None

def show_five_cities():
    results = []
    for city in CITIES:
        data = get_weather(city)
        if data:
            results.append(data)

    if results:
        temps = [r["temp"] for r in results]
        coldest = min(results, key=lambda x: x["temp"])
        avg_temp = statistics.mean(temps)

        output = "--- Weather for 5 cities ---\n"
        for r in results:
            output += f"{r['city']}: {r['condition']}, {r['temp']}°C, humidity {r['humidity']}% ({r['description']})\n"
        output += f"\nColdest city: {coldest['city']} ({coldest['temp']}°C)\n"
        output += f"Average temperature: {avg_temp:.2f}°C"

        text_output.delete(1.0, tk.END)
        text_output.insert(tk.END, output)

def show_single_city():
    city = entry_city.get().strip()
    if not city:
        messagebox.showwarning("Input Error", "Please enter a city name.")
        return
    data = get_weather(city)
    if data:
        output = f"{data['city']}: {data['condition']}\n"
        output += f"Temperature: {data['temp']}°C\n"
        output += f"Humidity: {data['humidity']}%\n"
        output += f"Description: {data['description']}"
        text_output.delete(1.0, tk.END)
        text_output.insert(tk.END, output)

# -------- GUI setup --------
root = tk.Tk()
root.title("Weather App")

frame_top = tk.Frame(root)
frame_top.pack(pady=10)

btn_five = tk.Button(frame_top, text="Show 5 Cities", command=show_five_cities)
btn_five.grid(row=0, column=0, padx=5)

entry_city = tk.Entry(frame_top, width=25)
entry_city.grid(row=0, column=1, padx=5)
btn_single = tk.Button(frame_top, text="Show City", command=show_single_city)
btn_single.grid(row=0, column=2, padx=5)

text_output = tk.Text(root, width=80, height=20)
text_output.pack(pady=10)

root.mainloop()
