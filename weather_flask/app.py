from flask import Flask, render_template, request
import requests
import statistics

app = Flask(__name__)

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
    except requests.RequestException:
        return None

@app.route("/", methods=["GET", "POST"])
def index():
    single_city = None
    results = []

    if request.method == "POST":
        city_input = request.form.get("city")
        if city_input:
            single_city = get_weather(city_input.strip())

    for city in CITIES:
        data = get_weather(city)
        if data:
            results.append(data)

    temps = [r["temp"] for r in results]
    coldest = min(results, key=lambda x: x["temp"]) if temps else None
    avg_temp = statistics.mean(temps) if temps else None

    return render_template("index.html",
                           results=results,
                           coldest=coldest,
                           avg_temp=avg_temp,
                           single_city=single_city)

if __name__ == "__main__":
    app.run(debug=True)
