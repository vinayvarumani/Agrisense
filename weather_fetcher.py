import requests
API_KEY = "52233c984359d112baf4b7990dfdaa10"

def get_weather(city):
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params ={
        "q": city ,
        "appid" : API_KEY,
        "units" : "metric"
    }

    try:
        response = requests.get(base_url , params = params)
        data = response.json()
        
        if data["cod"] != 200:
            return f"Error: {data['message']}"
        weather ={
            "city" : city.title(),
            "temperature" : data["main"]["temp"],
            "humidity" : data["main"]["humidity"],
            "weather" : data["weather"][0]["main"]
        }

        return weather
    except Exception as e:
        return f"Error fetching weather : {e}"

