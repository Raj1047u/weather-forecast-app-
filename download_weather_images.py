import os
import requests
from PIL import Image
from io import BytesIO

def download_image(url, save_path):
    """Download and save an image from URL"""
    try:
        response = requests.get(url)
        if response.status_code == 200:
            # Open and save the image
            img = Image.open(BytesIO(response.content))
            img.save(save_path)
            print(f"Successfully downloaded: {save_path}")
            return True
    except Exception as e:
        print(f"Error downloading {save_path}: {e}")
    return False

def main():
    # Create weather_images directory if it doesn't exist
    if not os.path.exists("weather_images"):
        os.makedirs("weather_images")
    
    # Weather images from Pexels (free to use)
    weather_images = {
        "clear_sky.jpg": "https://images.pexels.com/photos/912364/pexels-photo-912364.jpeg",
        "cloudy.jpg": "https://images.pexels.com/photos/1118873/pexels-photo-1118873.jpeg",
        "rainy.jpg": "https://images.pexels.com/photos/125510/pexels-photo-125510.jpeg",
        "drizzle.jpg": "https://images.pexels.com/photos/125510/pexels-photo-125510.jpeg",
        "thunderstorm.jpg": "https://images.pexels.com/photos/1169754/pexels-photo-1169754.jpeg",
        "snowy.jpg": "https://images.pexels.com/photos/688660/pexels-photo-688660.jpeg",
        "misty.jpg": "https://images.pexels.com/photos/1366630/pexels-photo-1366630.jpeg",
        "foggy.jpg": "https://images.pexels.com/photos/1366630/pexels-photo-1366630.jpeg",
        "hazy.jpg": "https://images.pexels.com/photos/1366630/pexels-photo-1366630.jpeg",
        "smoky.jpg": "https://images.pexels.com/photos/1366630/pexels-photo-1366630.jpeg",
        "dusty.jpg": "https://images.pexels.com/photos/1366630/pexels-photo-1366630.jpeg",
        "sandy.jpg": "https://images.pexels.com/photos/1366630/pexels-photo-1366630.jpeg",
        "ashy.jpg": "https://images.pexels.com/photos/1366630/pexels-photo-1366630.jpeg",
        "squall.jpg": "https://images.pexels.com/photos/1169754/pexels-photo-1169754.jpeg",
        "tornado.jpg": "https://images.pexels.com/photos/1169754/pexels-photo-1169754.jpeg"
    }
    
    # Download each image
    for filename, url in weather_images.items():
        save_path = os.path.join("weather_images", filename)
        if not os.path.exists(save_path):
            download_image(url, save_path)
        else:
            print(f"Image already exists: {save_path}")

if __name__ == "__main__":
    main() 