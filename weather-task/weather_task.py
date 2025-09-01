import requests
import statistics

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
        print(f"[ERROR] {city}: {e}")
        return None

def task_five_cities():
    results = []
    for city in CITIES:
        data = get_weather(city)
        if data:
            results.append(data)

    print("\n--- Weather for 5 cities ---")
    for r in results:
        print(f"{r['city']}: {r['condition']}, {r['temp']}°C, humidity {r['humidity']}% ({r['description']})")

    temps = [r["temp"] for r in results]
    if temps:
        coldest = min(results, key=lambda x: x["temp"])
        avg_temp = statistics.mean(temps)
        print(f"\nColdest city: {coldest['city']} ({coldest['temp']}°C)")
        print(f"Average temperature: {avg_temp:.2f}°C")

def task_single_city():
    city = input("Enter city name (e.g., 'Plovdiv,BG'): ").strip()
    if not city:
        print("No city entered.")
        return
    data = get_weather(city)
    if data:
        print(f"{data['city']}: {data['condition']}")
        print(f"Temperature: {data['temp']}°C")
        print(f"Humidity: {data['humidity']}%")
        print(f"Description: {data['description']}")
    else:
        print("Could not find data for this city.")

if __name__ == "__main__":
    while True:
        print("\n--- Menu ---")
        print("1) Five selected cities")
        print("2) Search individual city")
        print("3) Exit")
        choice = input("Choose an option (1/2/3): ").strip()
        if choice == "1":
            task_five_cities()
        elif choice == "2":
            task_single_city()
        elif choice == "3":
            break
        else:
            print("Invalid choice.")
