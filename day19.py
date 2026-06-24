from anthropic import Anthropic
from dotenv import load_dotenv
import os
import time

load_dotenv()

client = Anthropic(api_key = os.getenv("ANTHROPIC_API_KEY"))

def getTime():
    return time.strftime("%Y-%m-%d %H:%M:%S")

def askClaude(question = "What is the time"):
    response = client.messages.create(
        model = "claude-sonnet-4-6",
        max_tokens = 1024,
        tools = [{"name":"getTime",
                  "description": "Get the current time use this when user ask for time",
                  "input_schema": {
                      "type": "object",
                      "properties": {},

                  }}],
        messages = [
            {"role": "user", "content": question }
        ]
    )
    return response.content


def handleResponse():
    response = askClaude()
    if response[1].name == 'getTime':
        current_time = getTime()
    
    nextResponse = client.messages.create(
        model = "claude-sonnet-4-6",
        max_tokens = 1024,
        tools = [{"name":"getTime",
                  "description": "Get the current time use this when user ask for time",
                  "input_schema": {
                      "type": "object",
                      "properties": {},

                  }}],
        messages = [
            {"role": "user", "content": "What is the time" },
            {"role":"assistant", "content": response},
            {"role": "user", "content": [{
                "type": "tool_result",
                "tool_use_id": response[1].id,
                "content": current_time
            }]}
        ]
    )
    print(nextResponse.content)


handleResponse()
