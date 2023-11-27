import openai
import requests

# Your OpenAI API key
openai.api_key = "your_openai_api_key"

# Create an Agriculture Assistant
assistant = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are an expert agriculture Bot, Write and run code to answer advanced and basic agricultural questions."},
        {"role": "user", "content": "my plant is dying. Can you help me?"}
    ]
)

# Check if the user's message is an agricultural query
user_message = "my plant is dying. Can you help me?"

# Define keywords or patterns that indicate the user is asking about agriculture
agriculture_keywords = ['agriculture', 'crop', 'farming']

# Check if any of the keywords are present in the user's message
is_agricultural_query = any(keyword in user_message.lower() for keyword in agriculture_keywords)

if is_agricultural_query:
    # Send the message to the specialized endpoint for agricultural knowledge
    agriculture_response = requests.post(
        'https://api.example.com/agriculture',
        json={'message': user_message}
    )
    print(agriculture_response.json().get('response', 'Sorry, I don\'t have information on that right now.'))
else:
    # Send the message to the general ChatGPT endpoint
    general_response = openai.Completion.create(
        model="gpt-3.5-turbo",
        prompt=user_message
    )
    print(general_response.choices[0].text.strip())