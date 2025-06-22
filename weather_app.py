import requests
import os
import json
import sys
from datetime import datetime

# Check if API key is provided as command line argument or set in environment
if len(sys.argv) > 1:
    API_KEY = sys.argv[1]
else:
    API_KEY = os.environ.get("OPENWEATHER_API_KEY")
    if not API_KEY:
        print("Error: No API key provided")
        print("Usage: python weather_app.py <api_key>")
        print("Or set the OPENWEATHER_API_KEY environment variable")
        sys.exit(1)

BASE_URL = "https://api.openweathermap.org/data/2.5/"


def get_weather(city, country_code=None):
    """
    Get current weather for a city
    """
    location = city
    if country_code:
        location = f"{city},{country_code}"
        
    params = {
        "q": location,
        "appid": API_KEY,
        "units": "metric"  # Use metric by default
    }
    
    response = requests.get(f"{BASE_URL}weather", params=params)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return None


def get_forecast(city, country_code=None, days=5):
    """
    Get weather forecast for a city
    """
    location = city
    if country_code:
        location = f"{city},{country_code}"
        
    params = {
        "q": location,
        "appid": API_KEY,
        "units": "metric",
        "cnt": days * 8  # 8 forecasts per day (3-hour steps)
    }
    
    response = requests.get(f"{BASE_URL}forecast", params=params)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return None


def display_current_weather(data):
    """
    Display current weather in a formatted way
    """
    if not data:
        return
    
    city_name = data["name"]
    country = data["sys"]["country"]
    weather_main = data["weather"][0]["main"]
    weather_desc = data["weather"][0]["description"]
    temp = data["main"]["temp"]
    feels_like = data["main"]["feels_like"]
    humidity = data["main"]["humidity"]
    wind_speed = data["wind"]["speed"]
    
    sunrise_time = datetime.fromtimestamp(data["sys"]["sunrise"]).strftime("%H:%M")
    sunset_time = datetime.fromtimestamp(data["sys"]["sunset"]).strftime("%H:%M")
    
    print(f"\n{'=' * 40}")
    print(f"Current Weather for {city_name}, {country}")
    print(f"{'=' * 40}")
    print(f"Weather: {weather_main} - {weather_desc}")
    print(f"Temperature: {temp}°C (Feels like: {feels_like}°C)")
    print(f"Humidity: {humidity}%")
    print(f"Wind Speed: {wind_speed} m/s")
    print(f"Sunrise: {sunrise_time}")
    print(f"Sunset: {sunset_time}")
    print(f"{'=' * 40}\n")


def display_forecast(data):
    """
    Display weather forecast in a formatted way
    """
    if not data:
        return
    
    city_name = data["city"]["name"]
    country = data["city"]["country"]
    
    print(f"\n{'=' * 50}")
    print(f"5-Day Weather Forecast for {city_name}, {country}")
    print(f"{'=' * 50}")
    
    # Group forecasts by day
    current_date = ""
    for item in data["list"]:
        forecast_time = datetime.fromtimestamp(item["dt"])
        forecast_date = forecast_time.strftime("%Y-%m-%d")
        forecast_hour = forecast_time.strftime("%H:%M")
        
        if forecast_date != current_date:
            current_date = forecast_date
            print(f"\n{forecast_date} ({forecast_time.strftime('%A')})")
            print("-" * 50)
        
        weather_main = item["weather"][0]["main"]
        weather_desc = item["weather"][0]["description"]
        temp = item["main"]["temp"]
        
        print(f"{forecast_hour}: {temp}°C - {weather_main} ({weather_desc})")
    
    print(f"{'=' * 50}\n")


def main():
    print("Weather Forecast Application")
    print("---------------------------")
    
    while True:
        print("\nOptions:")
        print("1. Get current weather")
        print("2. Get 5-day forecast")
        print("3. Exit")
        
        choice = input("\nEnter your choice (1-3): ")
        
        if choice == "3":
            print("Goodbye!")
            break
        
        city = input("Enter city name: ")
        country_code = input("Enter country code (optional, press Enter to skip): ")
        if country_code.strip() == "":
            country_code = None
        
        if choice == "1":
            data = get_weather(city, country_code)
            display_current_weather(data)
        elif choice == "2":
            data = get_forecast(city, country_code)
            display_forecast(data)
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main() 