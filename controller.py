import requests
from datetime import datetime

class OpenWeather:
    def __init__(self, city):
        self.city = city

    def weather(self):
        url = f"https://api.openweathermap.org/data/2.5/weather?q={self.city},BR&appid=f19282a3fe5af10cce5eb39f29d767e0"
        
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            kelvin = data["main"]["temp"]
            celsius = kelvin - 273.15

            weather_data = {
                "cidade": self.city,
                "temperatura": round(celsius)
            }
            
            return weather_data
        except requests.exceptions.RequestException as e:
            print(f"Error occurred: {e}")


