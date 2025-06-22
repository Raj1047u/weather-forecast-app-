# Weather Forecast App

A Python application that fetches and displays weather data using the OpenWeatherMap API.

## Features

- Get current weather conditions for any city worldwide
- View 5-day weather forecasts with 3-hour intervals
- Console-based interface or graphical user interface
- Display of temperature, humidity, wind speed, sunrise/sunset times, and more

## Requirements

- Python 3.6+
- Required packages:
  - requests
  - python-dotenv
  - tkinter (included with Python, for GUI version)

## Installation

1. Clone or download this repository
2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Get your free API key from [OpenWeatherMap](https://openweathermap.org/appid)

## Usage

### Console Version

Run the console version of the app:

```
python weather_app.py <your_api_key>
```

Or set the API key as an environment variable:

```
# On Windows
set OPENWEATHER_API_KEY=your_api_key_here
python weather_app.py

# On macOS/Linux
export OPENWEATHER_API_KEY=your_api_key_here
python weather_app.py
```

### GUI Version

Run the graphical user interface version:

```
python weather_gui.py <your_api_key>
```

Or set the API key as an environment variable as shown above.

## How to Use

### Console Version
1. Choose an option from the menu (current weather, forecast, or exit)
2. Enter the city name
3. Optionally enter a country code (e.g., "US" for United States)
4. View the weather data

### GUI Version
1. Enter the city name in the input field
2. Optionally enter a country code
3. Click "Current Weather" or "5-Day Forecast" button
4. View the results in the respective tab

## API Documentation

This app uses the [OpenWeatherMap API](https://openweathermap.org/api). For more information, visit their documentation.

## License

This project is open source and available for personal and educational use. 