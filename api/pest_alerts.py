import requests


api_key ="48e0de57893a6c4b175c73482eb6bda3"


def current_weather(city):
    # api_url = f'http://api.weatherstack.com/current?access_key={api_key}&query={city}'
    # response = requests.get(api_url)
    # data = response.json()
    # return data
    api_key ="48e0de57893a6c4b175c73482eb6bda3"
    api_url = f"http://api.weatherstack.com/current"
    params = {"access_key": api_key, "query": city}
    
    try:
        response = requests.get(api_url,params=params)
        data = response.json()
        current_temp = data["current"]["temperature"]
        return current_temp
    except Exception as e:
        print(f"Error fetching weather data: {e}")
        return None

def check_pest_alert(crops, current_temp):
    pest_alerts = {
        "Corn": {"pest": "Corn Earworm", "temperature_range": (75, 90)},
        "Wheat": {"pest": "Hessian Fly", "temperature_range": (50, 75)},
        "Rice": {"pest": "Rice Weevil", "temperature_range": (70, 95)},
        "Barley": {"pest": "Aphid", "temperature_range": (70, 80)},
        "Sugarcane": {"pest": "Sugarcane Aphid", "temperature_range": (77, 95)},
        "Soybean": {"pest": "Soybean Aphid", "temperature_range": (60, 77)},
        "Tomatoes": {"pest": "Tomato Hornworm", "temperature_range": (70, 95)},
        "Carrots": {"pest": "Carrot Fly", "temperature_range": (50, 70)},
        "Cassava": {"pest": "Cassava Green Mite", "temperature_range": (68, 95)},
        "Yam": {"pest": "Yam Beetle", "temperature_range": (122, 158)},
        "Millet": {"pest": "Millet Head Miner", "temperature_range": (122, 158)},
        "Okra": {"pest": "Okra Aphid", "temperature_range": (122, 158)},
        "Cowpea": {"pest": "Cowpea Aphid", "temperature_range": (122, 158)},
        "Bitter Leaf": {"pest": "Bitter Leaf Aphid", "temperature_range": (122, 158)},
        "Maize": {"pest": "Maize Stalk Borer", "temperature_range": (122, 158)},
        "Rice": {"pest": "Rice Hispa", "temperature_range": (122, 158)},
        "Banana": {"pest": "Banana Aphid", "temperature_range": (80, 89.6)},
        "Apple": {"pest": "Codling Moth", "temperature_range": (64.4, 75.2)},
        "Watermelon": {"pest": "Watermelon Aphid", "temperature_range": (77, 95)},
        "Orange": {"pest": "Citrus Leafminer", "temperature_range": (59, 86)},
        "Plantains": {"pest": "Plantain Weevil", "temperature_range": (77, 86)},
        "Paw Paw": {"pest": "Pawpaw Fruit Fly", "temperature_range": (77, 95)},
        "Corn": {"pest": "Corn Earworm", "temperature_range": (75, 90)},
        "Strawberry": {"pest": "Strawberry Aphid", "temperature_range": (60, 77)},
        "Potato": {"pest": "Colorado Potato Beetle", "temperature_range": (45, 75)},
        "Cucumber": {"pest": "Cucumber Beetle", "temperature_range": (70, 90)},
        "Grapes": {"pest": "Grape Berry Moth", "temperature_range": (50, 90)},
        "Lettuce": {"pest": "Lettuce Aphid", "temperature_range": (50, 70)},
        "Watermelon": {"pest": "Watermelon Aphid", "temperature_range": (77, 95)},
        "Peach": {"pest": "Peach Aphid", "temperature_range": (50, 85)},
        "Avocado": {"pest": "Avocado Thrips", "temperature_range": (70, 90)},
        "Groundnut": {"pest": "Groundnut Aphid", "temperature_range": (77, 95)},
    }

    alerts = []
    for produce in crops:      
        if produce in pest_alerts:
            pest_data = pest_alerts[produce]
            pest_name = pest_data["pest"]
            temp_range = pest_data["temperature_range"]

            if temp_range[0] <= current_temp <= temp_range[1]:
                alert = f"Alert: {pest_name} infestation possible for {produce}."
                alerts.append(alert)
            else:
                alert = f"No Pest alerts at the moment for {produce}! You are good to go!"
    
    return alerts
    
