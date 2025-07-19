# Final Project - Weather Dashboard v1
import requests
import csv
from datetime import datetime

API_KEY = "5969c823fc2f9fdad353f59eb336a5ca"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
LOG_FILE = "weather_log.csv"

class WeatherReport:
    def __init__(self, city, temp_f, humidity, wind_speed, condition):
        self.city = city
        self.temp_f = temp_f
        self.humidity = humidity
        self.wind_speed = wind_speed
        self.condition = condition
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def display(self):
        print(f"\nWeather in {self.city} at {self.timestamp}")
        print(f"Temperature: {self.temp_f}°F")
        print(f"Humidity: {self.humidity}%")
        print(f"Wind speed: {self.wind_speed}mph")

    def log_to_file(self):
        with open(LOG_FILE, "a", newline="") as f:
            writer = csv.writer(f)
            if f.tell() == 0:
                writer.writerow(["Timestamp", "City", "Temperature (F)", "Condition", "Humidity", "Wind Speed (mph)"])
            writer.writerow([self.timestamp, self.city, self.temp_f, self.condition, self.humidity, self.wind_speed])

def fetch_weather(city):
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "imperial", # Fahrenheit
    }
    try:
        response = requests.get(BASE_URL, params=params)
        print("-> Requesting:", response.url)
        data = response.json()

        if response.status_code != 200:
            print("Error:", data.get("message", "Failed to retrieve data"))
            return None

        weather = WeatherReport(
            city=data["name"],
            temp_f=data["main"]["temp"],
            humidity=data["main"]["humidity"],
            wind_speed=data["wind"]["speed"],
            condition=data["weather"][0]["description"].title()
        )
        return weather
    except Exception as e:
        print("Request Failed:", e)
        return None

def main():
    print("Welcome to the Weather Dashboard CLI")
    while True:
        city = input("\nEnter a city name (or type 'exit' to quit): ").strip()
        if city.lower() == "exit":
            print("Goodbye!")
            break
        report = fetch_weather(city)
        if report:
            report.display()
            report.log_to_file()

if __name__ == "__main__":
    main()