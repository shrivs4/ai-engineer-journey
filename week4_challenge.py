from anthropic import Anthropic
from dotenv import load_dotenv
import os

load_dotenv()
client = Anthropic(api_key = os.getenv('ANTHROPIC_API_KEY'))

def get_weather(city):
    return f"The weather in {city} is 28°C and sunny"

available_tools = {
    "get_weather": get_weather
}

tool_description = [
    {
        "name": "get_weather",
        "description": "This function is used to reterive the proivded city weather",
        "input_schema":{
            "type": "object",
            "properties":{
                "city":{
                    "type": "string",
                    "description": "This function will take arguments as city name"
                },
            },
            "required": ["city"]
        }
    }
]

def call_anthropic():
    response = client.messages.create(
        model = "claude-sonnet-4-6",
        max_tokens = 1024,
        tools = tool_description,
        messages = [{
            "role": "user",
            "content": "Compare the weather in Tokyo and London."
        }]
        )
    tool_call = None
    messages_list = [{
            "role": "user",
            "content": "Compare the weather in Tokyo and London."
        }]
    tool_use_status = response.stop_reason
    final_response = response
    while tool_use_status == "tool_use":
        results = []
        for block in final_response.content:
            if(block.type == "tool_use"):
                function_to_call = available_tools[block.name]
                result = function_to_call(**block.input)
                results.append({
                    "id": block.id,
                    "result": result 
                })
        messages_list.append({
            "role": "assistant", "content": final_response.content
        })
        content = []
        for item in results:
            data = {
                "type": "tool_result",
                "tool_use_id": item["id"],
                "content": item["result"]
            }
            content.append(data)
        messages_list.append({
            "role": "user",
            "content": content
        })
        final_response = client.messages.create(
            model = "claude-sonnet-4-6",
            max_tokens = 1024,
            tools = tool_description,
            messages = messages_list
        )
        tool_use_status = final_response.stop_reason

    print(final_response.content)



    

call_anthropic()

