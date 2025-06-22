import urllib.request
import os

def download_image(url, filename):
    try:
        urllib.request.urlretrieve(url, filename)
        print(f"Downloaded {filename}")
    except Exception as e:
        print(f"Error downloading {filename}: {e}")

# Create backgrounds directory if it doesn't exist
if not os.path.exists("backgrounds"):
    os.makedirs("backgrounds")

# Download background images
backgrounds = {
    "dawn.jpg": "https://raw.githubusercontent.com/your-username/weather-app/main/backgrounds/dawn.jpg",
    "day.jpg": "https://raw.githubusercontent.com/your-username/weather-app/main/backgrounds/day.jpg",
    "dusk.jpg": "https://raw.githubusercontent.com/your-username/weather-app/main/backgrounds/dusk.jpg",
    "night.jpg": "https://raw.githubusercontent.com/your-username/weather-app/main/backgrounds/night.jpg"
}

for filename, url in backgrounds.items():
    download_image(url, os.path.join("backgrounds", filename)) 