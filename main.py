import os
os.environ['OPENAI_API_KEY'] = ''

import openai
from openai import OpenAI
import json

# Set up your OpenAI API key
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

functions = [
    # get weather Information
    {
        "name": "get_weather",  # Name of the function
        "description": "Get the current weather in a location",  # Description of what the function does
        "parameters": {  # Define the parameters the function expects
            "type": "object",
            "properties": {
                "location": {"type": "string", "description": "The city and state, e.g. San Francisco, CA"},
                # The location parameter
            },
            "required": ["location"]  # The location parameter is required
        }
    },

    # get current time
    {
        "name": "get_current_time",
        "description": "Get the current time",
        "parameters": {
            "type": "object",
            "properties": {}
        }
    }
]

prompt = "What's the weather like in Frisco?"  # prompt to test call get_weather function

response = client.chat.completions.create(
    model="gpt-4o-mini",  # Specify the model to use
    messages=[{"role": "user", "content": prompt}],  # The user's input message
    functions=functions,  # The list of functions defined above
    function_call="auto"  # Automatically call the appropriate function based on the user's input
)

def get_my_weather(location):
    #  Implement your function here
    temp = 25
    return f"The weather in {location} is sunny and {temp} degrees ."


function_call = response.choices[0].message.function_call

if function_call and function_call.name == "get_weather":
     # Parse the arguments from the function call
     arguments = json.loads(function_call.arguments)
     # Call the get_weather function with the parsed arguments and print the result
     weather_result = get_my_weather(arguments["location"])
     print(f"Weather: {weather_result}")

