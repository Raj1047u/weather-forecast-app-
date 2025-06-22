import tkinter as tk
import customtkinter as ctk
from tkinter import ttk, messagebox
import requests
import os
import sys
from datetime import datetime, timedelta
import threading
from PIL import Image, ImageTk
import io
import urllib.request
from ttkthemes import ThemedTk
import json
import random

class WeatherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Weather Forecast App")
        self.root.geometry("800x600")
        self.root.minsize(800, 600)
        self.root.configure(bg="#f0f0f0")
        
        # API Key handling
        self.API_KEY = "af999707ba5f21c8b5a39de39386d146" or os.environ.get("OPENWEATHER_API_KEY")
        if not self.API_KEY:
            messagebox.showerror("API Key Error", "No OpenWeather API key provided. Please set it in the code or as the OPENWEATHER_API_KEY environment variable.")
            self.root.destroy()
            return
        self.BASE_URL = "https://api.openweathermap.org/data/2.5/"
        
        self.icons = {}  # Cache for weather icons
        self.backgrounds = {}  # Cache for backgrounds
        self.weather_images = {}
        self.current_bg_image = None
        
        # Configure customtkinter
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Load weather image mappings
        self.load_weather_images()
        
        # Set up the UI
        self.setup_ui()
        
        # Set initial background
        self.update_background()
    
    def load_weather_images(self):
        """Load weather images from the weather_images directory"""
        image_dir = "weather_images"
        if not os.path.exists(image_dir):
            os.makedirs(image_dir)
            
        # Default weather conditions and their corresponding image names
        self.weather_mappings = {
            "Clear": "clear_sky.jpg",
            "Clouds": "cloudy.jpg",
            "Rain": "rainy.jpg",
            "Drizzle": "drizzle.jpg",
            "Thunderstorm": "thunderstorm.jpg",
            "Snow": "snowy.jpg",
            "Mist": "misty.jpg",
            "Fog": "foggy.jpg",
            "Haze": "hazy.jpg",
            "Smoke": "smoky.jpg",
            "Dust": "dusty.jpg",
            "Sand": "sandy.jpg",
            "Ash": "ashy.jpg",
            "Squall": "squall.jpg",
            "Tornado": "tornado.jpg"
        }
        
        # Load all available images
        for weather, image_name in self.weather_mappings.items():
            image_path = os.path.join(image_dir, image_name)
            if os.path.exists(image_path):
                try:
                    image = Image.open(image_path)
                    self.weather_images[weather] = image
                except Exception as e:
                    print(f"Error loading image {image_name}: {e}")
    
    def get_time_based_background(self):
        """Get background based on time of day"""
        current_hour = datetime.now().hour
        
        if 5 <= current_hour < 7:  # Dawn
            return os.path.join(os.path.dirname(os.path.abspath(__file__)), "backgrounds", "dawn.jpg")
        elif 7 <= current_hour < 17:  # Day
            return os.path.join(os.path.dirname(os.path.abspath(__file__)), "backgrounds", "day.jpg")
        elif 17 <= current_hour < 19:  # Dusk
            return os.path.join(os.path.dirname(os.path.abspath(__file__)), "backgrounds", "dusk.jpg")
        else:  # Night
            return os.path.join(os.path.dirname(os.path.abspath(__file__)), "backgrounds", "night.jpg")
    
    def get_weather_background(self, weather_condition):
        """Get background based on weather condition (customized for sunny, rain, etc.)"""
        # Normalize condition
        condition = weather_condition.lower()
        if condition in ["clear", "clouds", "sunny"]:
            image_name = "sunny.jpg"
        elif condition in ["rain", "drizzle", "thunderstorm"]:
            image_name = "rain.jpg"
        else:
            image_name = "sunny.jpg"  # Default fallback
        return os.path.join(os.path.dirname(os.path.abspath(__file__)), "backgrounds", image_name)
    
    def update_background(self, weather_condition=None):
        """Update the background based on weather condition or time of day"""
        try:
            if weather_condition:
                # Get background based on weather condition
                bg_path = self.get_weather_background(weather_condition)
            else:
                # Get background based on time of day
                bg_path = self.get_time_based_background()
            
            print(f"Attempting to load background from: {bg_path}")
            
            # Check if file exists
            if not os.path.exists(bg_path):
                print(f"Background file not found: {bg_path}")
                self.bg_label.configure(image="")
                self.bg_label.configure(fg_color="#2b2b2b")
                return
            
            # Load and resize image
            image = Image.open(bg_path)
            window_width = self.root.winfo_width()
            window_height = self.root.winfo_height()
            
            if window_width > 1 and window_height > 1:
                # Calculate aspect ratio
                img_width, img_height = image.size
                aspect_ratio = img_width / img_height
                
                # Resize image to fit window while maintaining aspect ratio
                if window_width / window_height > aspect_ratio:
                    new_height = window_height
                    new_width = int(new_height * aspect_ratio)
                else:
                    new_width = window_width
                    new_height = int(new_width / aspect_ratio)
                
                image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
                
                # Convert to CTkImage
                photo = ctk.CTkImage(
                    light_image=image,
                    dark_image=image,
                    size=(new_width, new_height)
                )
                
                # Update background label
                self.bg_label.configure(image=photo)
                self.bg_label._image = photo  # Keep a reference
                print(f"Successfully loaded and displayed background: {bg_path}")
                
                # Schedule next update
                self.root.after(3600000, self.update_background)  # Update every hour
            
        except Exception as e:
            print(f"Error updating background: {str(e)}")
            # Fallback to a solid color
            self.bg_label.configure(image="")
            self.bg_label.configure(fg_color="#2b2b2b")
    
    def setup_ui(self):
        """Set up the user interface"""
        # Configure window
        self.root.title("Weather Forecast")
        self.root.geometry("1200x800")
        
        # Create main frame
        self.main_frame = ctk.CTkFrame(self.root)
        self.main_frame.pack(fill="both", expand=True)
        
        # Create background label
        self.bg_label = ctk.CTkLabel(self.main_frame, text="")
        self.bg_label.place(relwidth=1, relheight=1)
        
        # Show intro background
        self.show_intro_background()
        
        # Create content frame with transparency
        self.content_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Welcome message
        welcome_label = ctk.CTkLabel(
            self.content_frame,
            text="Weather Forecast",
            font=("Helvetica", 24, "bold")
        )
        welcome_label.pack(pady=20)
        
        # Input frame
        input_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        input_frame.pack(fill="x", pady=10)
        
        # City input
        city_label = ctk.CTkLabel(input_frame, text="City:")
        city_label.pack(side="left", padx=5)
        
        self.city_var = tk.StringVar()
        self.city_entry = ctk.CTkEntry(
            input_frame,
            textvariable=self.city_var,
            width=300
        )
        self.city_entry.pack(side="left", padx=5)
        
        # Country code input
        country_label = ctk.CTkLabel(input_frame, text="Country Code:")
        country_label.pack(side="left", padx=5)
        
        self.country_var = tk.StringVar()
        self.country_entry = ctk.CTkEntry(
            input_frame,
            textvariable=self.country_var,
            width=10
        )
        self.country_entry.pack(side="left", padx=5)
        
        # Bind Enter key to search_weather
        self.city_entry.bind("<Return>", lambda event: self.search_weather())
        
        # Get weather button
        self.weather_btn = ctk.CTkButton(
            input_frame,
            text="Get Weather",
            command=self.search_weather
        )
        self.weather_btn.pack(side="left", padx=5)
        
        # Create tabview
        self.notebook = ctk.CTkTabview(self.content_frame)
        self.notebook.pack(fill="both", expand=True, pady=10)
        
        # Add tabs
        self.notebook.add("Current Weather")
        self.notebook.add("5-Day Forecast")
        
        # Create canvas for current weather
        self.current_canvas = tk.Canvas(
            self.notebook.tab("Current Weather"),
            bg="#ffffff",
            highlightthickness=0
        )
        self.current_canvas.pack(fill="both", expand=True)
        
        # Create canvas for 5-day forecast
        self.forecast_canvas = tk.Canvas(
            self.notebook.tab("5-Day Forecast"),
            bg="#ffffff",
            highlightthickness=0
        )
        self.forecast_canvas.pack(fill="both", expand=True)
        
        # Add scrollbars
        current_scrollbar = ttk.Scrollbar(self.notebook.tab("Current Weather"), orient="vertical", command=self.current_canvas.yview)
        current_scrollbar.pack(side="right", fill="y")
        self.current_canvas.configure(yscrollcommand=current_scrollbar.set)
        
        forecast_scrollbar = ttk.Scrollbar(self.notebook.tab("5-Day Forecast"), orient="vertical", command=self.forecast_canvas.yview)
        forecast_scrollbar.pack(side="right", fill="y")
        self.forecast_canvas.configure(yscrollcommand=forecast_scrollbar.set)
        
        # Bind mouse wheel to forecast canvas
        self.forecast_canvas.bind_all("<MouseWheel>", self._on_forecast_mousewheel)
        self.forecast_canvas.bind_all("<Button-4>", self._on_forecast_mousewheel)  # For Linux
        self.forecast_canvas.bind_all("<Button-5>", self._on_forecast_mousewheel)  # For Linux
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        status_label = ctk.CTkLabel(
            self.content_frame,
            textvariable=self.status_var,
            font=("Helvetica", 10)
        )
        status_label.pack(side="bottom", pady=5)
        
        # Set initial background
        self.root.after(100, self.update_background)  # Delay initial background update
        
        # Bind resize event
        self.root.bind("<Configure>", self._on_resize)
    
    def _on_resize(self, event):
        """Handle window resize event"""
        if event.widget == self.root:
            # Update canvas scroll region
            self.current_canvas.configure(scrollregion=self.current_canvas.bbox("all"))
            self.forecast_canvas.configure(scrollregion=self.forecast_canvas.bbox("all"))
            # Update background
            self.update_background()
    
    def get_weather_icon(self, icon_code):
        if icon_code in self.icons:
            return self.icons[icon_code]
        
        try:
            url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
            image_data = urllib.request.urlopen(url).read()
            image = Image.open(io.BytesIO(image_data))
            photo = ImageTk.PhotoImage(image)
            self.icons[icon_code] = photo
            return photo
        except:
            return None
    
    def display_current_weather(self, data):
        """Display current weather information in a Google-like style"""
        # Clear previous content
        self.current_canvas.delete("all")
        
        # Get weather data
        temp = data['main']['temp']
        feels_like = data['main']['feels_like']
        humidity = data['main']['humidity']
        wind_speed = data['wind']['speed']
        description = data['weather'][0]['description'].capitalize()
        city_name = data['name']
        country = data['sys']['country']
        
        # Calculate canvas dimensions
        canvas_width = self.current_canvas.winfo_width()
        canvas_height = self.current_canvas.winfo_height()
        
        # Create main weather card
        card_width = min(900, canvas_width - 40)
        card_height = min(700, canvas_height - 40)
        x = (canvas_width - card_width) // 2
        y = (canvas_height - card_height) // 2
        
        # Draw card background with rounded corners
        self.current_canvas.create_rectangle(
            x, y, x + card_width, y + card_height,
            fill="#ffffff", outline="", tags="card"
        )
        
        # Add location and time
        self.current_canvas.create_text(
            x + 20, y + 20,
            text=f"{city_name}, {country}",
            font=("Helvetica", 24, "bold"),
            fill="#202124",
            anchor="w",
            tags="card"
        )
        
        self.current_canvas.create_text(
            x + 20, y + 50,
            text=datetime.now().strftime("%A, %B %d, %I:%M %p"),
            font=("Helvetica", 14),
            fill="#5f6368",
            anchor="w",
            tags="card"
        )
        
        # Add main weather info
        self.current_canvas.create_text(
            x + 20, y + 100,
            text=f"{temp:.1f}°C",
            font=("Helvetica", 48, "bold"),
            fill="#202124",
            anchor="w",
            tags="card"
        )
        
        self.current_canvas.create_text(
            x + 20, y + 160,
            text=description,
            font=("Helvetica", 20),
            fill="#5f6368",
            anchor="w",
            tags="card"
        )
        
        self.current_canvas.create_text(
            x + 20, y + 190,
            text=f"Feels like {feels_like:.1f}°C",
            font=("Helvetica", 16),
            fill="#5f6368",
            anchor="w",
            tags="card"
        )
        
        # Add weather details in a grid
        details_x = x + 20
        details_y = y + 250
        detail_width = (card_width - 40) // 2
        detail_height = 100
        
        # Overview
        self._create_detail_box(
            details_x, details_y,
            detail_width, detail_height,
            "Overview",
            f"Temperature: {temp:.1f}°C\nFeels like: {feels_like:.1f}°C",
            "#f8f9fa"
        )
        
        # Precipitation
        self._create_detail_box(
            details_x + detail_width, details_y,
            detail_width, detail_height,
            "Precipitation",
            f"Humidity: {humidity}%\nPressure: {data['main']['pressure']} hPa",
            "#f8f9fa"
        )
        
        # Wind
        self._create_detail_box(
            details_x, details_y + detail_height,
            detail_width, detail_height,
            "Wind",
            f"Speed: {wind_speed} m/s\nDirection: {self._get_wind_direction(data['wind']['deg'])}",
            "#f8f9fa"
        )
        
        # Visibility
        self._create_detail_box(
            details_x + detail_width, details_y + detail_height,
            detail_width, detail_height,
            "Visibility",
            f"Distance: {data['visibility'] / 1000:.1f} km\nClouds: {data['clouds']['all']}%",
            "#f8f9fa"
        )
        
        # Add hourly forecast
        forecast_y = details_y + detail_height * 2 + 20
        self.current_canvas.create_text(
            x + 20, forecast_y,
            text="Hourly Forecast",
            font=("Helvetica", 18, "bold"),
            fill="#202124",
            anchor="w",
            tags="card"
        )
        
        # Create scrollable frame for hourly forecast
        forecast_frame = tk.Frame(self.current_canvas, bg="#ffffff")
        self.current_canvas.create_window(
            x + 20, forecast_y + 30,
            window=forecast_frame,
            anchor="nw",
            width=card_width - 40,
            height=200,
            tags="card"
        )
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(forecast_frame, orient="horizontal")
        scrollbar.pack(side="bottom", fill="x")
        
        # Create canvas for hourly forecast
        forecast_canvas = tk.Canvas(
            forecast_frame,
            bg="#ffffff",
            highlightthickness=0,
            xscrollcommand=scrollbar.set
        )
        forecast_canvas.pack(side="top", fill="both", expand=True)
        scrollbar.config(command=forecast_canvas.xview)
        
        # Add hourly forecast items
        forecast_width = 0
        for hour in range(24):
            hour_time = datetime.now() + timedelta(hours=hour)
            temp = temp + random.uniform(-2, 2)  # Simulate temperature variation
            
            # Create hour box
            box_width = 100
            box_height = 150
            box_x = hour * (box_width + 10)
            
            # Draw hour box
            forecast_canvas.create_rectangle(
                box_x, 0, box_x + box_width, box_height,
                fill="#f8f9fa", outline="#dadce0",
                tags="forecast"
            )
            
            # Add time
            forecast_canvas.create_text(
                box_x + box_width//2, 20,
                text=hour_time.strftime("%I %p"),
                font=("Helvetica", 12),
                fill="#5f6368",
                tags="forecast"
            )
            
            # Add temperature
            forecast_canvas.create_text(
                box_x + box_width//2, 60,
                text=f"{temp:.1f}°C",
                font=("Helvetica", 16, "bold"),
                fill="#202124",
                tags="forecast"
            )
            
            # Add weather icon (simplified)
            forecast_canvas.create_text(
                box_x + box_width//2, 100,
                text="☀️" if hour < 12 else "🌙",
                font=("Helvetica", 24),
                tags="forecast"
            )
            
            forecast_width = box_x + box_width + 10
        
        # Configure scroll region
        forecast_canvas.configure(scrollregion=(0, 0, forecast_width, box_height))
        
        # Update status
        self.status_var.set(f"Current weather displayed for {city_name}, {country}")

    def _create_detail_box(self, x, y, width, height, title, content, bg_color="#f8f9fa"):
        """Create a detail box with title and content"""
        # Draw box background
        self.current_canvas.create_rectangle(
            x, y, x + width, y + height,
            fill=bg_color, outline="#dadce0",
            tags="card"
        )
        
        # Add title
        self.current_canvas.create_text(
            x + 10, y + 15,
            text=title,
            font=("Helvetica", 14, "bold"),
            fill="#202124",
            anchor="w",
            tags="card"
        )
        
        # Add content
        self.current_canvas.create_text(
            x + 10, y + 45,
            text=content,
            font=("Helvetica", 12),
            fill="#5f6368",
            anchor="w",
            tags="card"
        )

    def _get_wind_direction(self, degrees):
        """Convert wind degrees to direction"""
        directions = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']
        index = round(degrees / 45) % 8
        return directions[index]
    
    def search_weather(self):
        city = self.city_var.get().strip()
        country = self.country_var.get().strip()
        
        if not city:
            messagebox.showerror("Error", "Please enter a city name")
            return
        
        location = city
        if country:
            location = f"{city},{country}"
        
        # Get current weather
        current_data = self.get_weather(location)
        if current_data:
            # Update background based on weather
            weather_main = current_data['weather'][0]['main']
            self.update_background(weather_main)
            self.display_current_weather(current_data)
        
        # Get forecast
        forecast_data = self.get_forecast(location)
        if forecast_data:
            self.display_forecast(forecast_data)
    
    def get_weather(self, location):
        params = {
            "q": location,
            "appid": self.API_KEY,
            "units": "metric"
        }
        
        try:
            response = requests.get(f"{self.BASE_URL}weather", params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", f"Failed to get weather data: {str(e)}")
            return None
    
    def get_forecast(self, location):
        params = {
            "q": location,
            "appid": self.API_KEY,
            "units": "metric",
            "cnt": 40  # 5 days * 8 forecasts per day
        }
        
        try:
            response = requests.get(f"{self.BASE_URL}forecast", params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", f"Failed to get forecast data: {str(e)}")
            return None
    
    def display_forecast(self, data):
        """Display 5-day forecast information"""
        # Clear previous content
        self.forecast_canvas.delete("all")
        
        # Calculate canvas dimensions
        canvas_width = self.forecast_canvas.winfo_width()
        canvas_height = self.forecast_canvas.winfo_height()
        
        # Create main forecast card
        card_width = min(900, canvas_width - 40)
        card_height = min(700, canvas_height - 40)
        x = (canvas_width - card_width) // 2
        y = (canvas_height - card_height) // 2
        
        # Draw card background
        self.forecast_canvas.create_rectangle(
            x, y, x + card_width, y + card_height,
            fill="#ffffff", outline="", tags="card"
        )
        
        # Add location
        self.forecast_canvas.create_text(
            x + 20, y + 20,
            text=f"5-Day Forecast for {data['city']['name']}, {data['city']['country']}",
            font=("Helvetica", 24, "bold"),
            fill="#202124",
            anchor="w",
            tags="card"
        )
        
        # Group forecasts by day
        current_date = None
        y_position = y + 80
        card_height = 120
        card_width = card_width - 40
        
        for item in data['list']:
            forecast_time = datetime.fromtimestamp(item['dt'])
            forecast_date = forecast_time.strftime("%Y-%m-%d")
            
            if forecast_date != current_date:
                current_date = forecast_date
                y_position += 20  # Add space between days
                
                # Draw date header
                self.forecast_canvas.create_text(
                    x + 20, y_position,
                    text=f"{forecast_time.strftime('%A, %B %d')}",
                    font=("Helvetica", 16, "bold"),
                    fill="#202124",
                    anchor="w",
                    tags="card"
                )
                y_position += 30
            
            # Draw forecast card
            self.forecast_canvas.create_rectangle(
                x + 20, y_position,
                x + 20 + card_width, y_position + card_height,
                fill="#f8f9fa", outline="#dadce0",
                tags="card"
            )
            
            # Add time
            self.forecast_canvas.create_text(
                x + 40, y_position + 20,
                text=forecast_time.strftime("%I:%M %p"),
                font=("Helvetica", 14, "bold"),
                fill="#202124",
                anchor="w",
                tags="card"
            )
            
            # Add temperature
            temp = item['main']['temp']
            feels_like = item['main']['feels_like']
            self.forecast_canvas.create_text(
                x + 200, y_position + 20,
                text=f"{temp:.1f}°C",
                font=("Helvetica", 16, "bold"),
                fill="#202124",
                anchor="w",
                tags="card"
            )
            
            self.forecast_canvas.create_text(
                x + 200, y_position + 45,
                text=f"Feels like {feels_like:.1f}°C",
                font=("Helvetica", 12),
                fill="#5f6368",
                anchor="w",
                tags="card"
            )
            
            # Add weather description
            description = item['weather'][0]['description'].capitalize()
            self.forecast_canvas.create_text(
                x + 400, y_position + 20,
                text=description,
                font=("Helvetica", 14),
                fill="#5f6368",
                anchor="w",
                tags="card"
            )
            
            # Add details
            humidity = item['main']['humidity']
            wind_speed = item['wind']['speed']
            self.forecast_canvas.create_text(
                x + 600, y_position + 20,
                text=f"Humidity: {humidity}%",
                font=("Helvetica", 12),
                fill="#5f6368",
                anchor="w",
                tags="card"
            )
            
            self.forecast_canvas.create_text(
                x + 600, y_position + 45,
                text=f"Wind: {wind_speed} m/s",
                font=("Helvetica", 12),
                fill="#5f6368",
                anchor="w",
                tags="card"
            )
            
            y_position += card_height + 10
        
        # Update scroll region
        self.forecast_canvas.configure(scrollregion=self.forecast_canvas.bbox("all"))

    def _on_forecast_mousewheel(self, event):
        # Windows and MacOS
        if event.num == 5 or event.delta == -120:
            self.forecast_canvas.yview_scroll(1, "units")
        elif event.num == 4 or event.delta == 120:
            self.forecast_canvas.yview_scroll(-1, "units")
        elif event.delta:
            # For finer scrolling on some systems
            self.forecast_canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def show_intro_background(self):
        """Show the intro background image and set theme accordingly"""
        try:
            intro_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "backgrounds", "intro.jpg")
            if os.path.exists(intro_path):
                image = Image.open(intro_path)
                window_width = self.root.winfo_width()
                window_height = self.root.winfo_height()
                if window_width > 1 and window_height > 1:
                    img_width, img_height = image.size
                    aspect_ratio = img_width / img_height
                    if window_width / window_height > aspect_ratio:
                        new_height = window_height
                        new_width = int(new_height * aspect_ratio)
                    else:
                        new_width = window_width
                        new_height = int(new_width / aspect_ratio)
                    image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
                    photo = ctk.CTkImage(
                        light_image=image,
                        dark_image=image,
                        size=(new_width, new_height)
                    )
                    self.bg_label.configure(image=photo)
                    self.bg_label._image = photo
        except Exception as e:
            print(f"Error loading intro background: {e}")

if __name__ == "__main__":
    root = ThemedTk(theme="arc")  # Use a modern theme
    app = WeatherApp(root)
    root.mainloop() 