import requests


WEATHERSTACK_API_KEY = '48e0de57893a6c4b175c73482eb6bda3'


def get_weather(city):
    base_url = "http://api.weatherstack.com/forecast?"
    params = {"access_key": WEATHERSTACK_API_KEY, "query": city}

    response = requests.get(base_url, params=params)
    data = response.json()

    return data