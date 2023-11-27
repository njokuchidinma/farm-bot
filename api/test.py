import requests


API_KEY = '48e0de57893a6c4b175c73482eb6bda3'

def get_weather_data(location):
    api_url = f'http://api.weatherstack.com/current?access_key={API_KEY}&query={location}'
    response = requests.get(api_url)
    data = response.json()
    return data

def check_pest_alerts(weather_data, produce_type):
    # Your logic to check for pest alerts based on weather and produce type
    # Example: If temperature is high and produce_type is susceptible to certain pests, generate alert
    temperature = weather_data.get('current', {}).get('temperature', 0)
    
    if temperature > 30 and produce_type == 'Tomato':
        return True  # Pest alert

    return False  # No pest alert

def generate_pest_alert(location, produce_type):
    weather_data = get_weather_data(location)

    if check_pest_alerts(weather_data, produce_type):
        # Your logic to notify the farmer about pest alert
        notification_message = f'Pest alert for {produce_type} in {location}. Take necessary actions.'
        print(notification_message)
        # You can send a notification using Django's signals or any other method

# Example usage:
location = 'your_farm_location'  # Replace with the actual location
produce_type = 'Tomato'  # Replace with the actual produce type

generate_pest_alert(location, produce_type)




import requests

def get_current_temperature(api_key, location):
    """
    Get the current temperature from the Weatherstack API.

    Args:
    - api_key (str): Your Weatherstack API key.
    - location (str): Location for weather information.

    Returns:
    - float: Current temperature in Fahrenheit.
    """
    api_key = '48e0de57893a6c4b175c73482eb6bda3'
    api_url = f"http://api.weatherstack.com/current"
    params = {"access_key": api_key, "query": location}
    
    try:
        response = requests.get(api_url, params=params)
        data = response.json()
        current_temperature = data["current"]["temperature"]
        return current_temperature
    except Exception as e:
        print(f"Error fetching weather data: {e}")
        return None



def check_pest_alert_for_temperature(produce, current_temperature):
    """
    Internal function to check pest alerts based on temperature.
    (Similar to the previous version of check_pest_alert)

    Returns:
    - str: Alert message.
    """
    # ... (same as previous version)

# Example usage:
api_key = "your_weatherstack_api_key"
location = "your_location"  # e.g., "City, Country"
produce_type = "Wheat"  # Change this to the specific produce type

alert_message = check_pest_alert(api_key, location, produce_type)
print(alert_message)



import requests




OpenAI-Beta: assistants=v1


assistant = client.beta.ssistants.create(
    name="AgricBot",
    instructions="You are an expert agriculture Bot, Write and run code to answer advance and bsdic agricultural questions. ",
    tools=[{"type": "code_interpreter"}],
    model="gpt-3.5-turbo-1106-"
)

thread = client.beta.threads.create()

message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content="my plant is dying. Can you help me?"
)

run = client.beta.threads.runs.create(
    thread_id=thread.id,
    assistant_id =assistant.id
    instructions="please adress user as Farmer. This user is logged an registered as a farmer"
)

run = client.beta.threads.runs.retrieve(
    thread_id=thread.id
    run_id=run.id
)

messages = client.beta.threads.messages.list(
  thread_id=thread.id
)