import os
from dotenv import load_dotenv
from tavily import TavilyClient
from anthropic import Anthropic
import json

load_dotenv()

client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
claude_client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def search_web(query):
    response = client.search(query)
    result_data = []
    for result in response["results"]:
        result_data.append({"title":result["title"],"content":result["content"]})
    return result_data

required_tools = {
    "search_web": search_web
}

tool_description = [
    {
        "name": "search_web",
        "description": "Search the internet for current, real-time, or recent information — use this when the answer requires up-to-date facts not in your training data.",
        "input_schema": {
            "type":"object",
            "properties" :{
                "query": {
                    "type": "string",
                    "description": "This could be any question eg: where is italy"
                }
            },
            "required": ["query"]
        } 
    }
]

def call_anthropic(query):
    response = claude_client.messages.create(
        model = "claude-sonnet-4-6",
        max_tokens = 1024,
        tools = tool_description,
        messages = [{
            "role": "user",
            "content": query
        }]
    )
    message_list = [{
        "role": "user",
        "content": query
    }]
    tool_use_status = response.stop_reason
    final_response = response
    while tool_use_status == "tool_use":
        results = []
        for block in final_response.content:
            if(block.type == "tool_use"):
                function_to_call = required_tools[block.name]
                result = function_to_call(**block.input)
                results.append({
                    "id": block.id,
                    "result": json.dumps(result)
                })
        message_list.append({
            "role":"assistant", "content": final_response.content 
        })

        content = []
        for item in results:
            data = {
                "type": "tool_result",
                "tool_use_id": item["id"],
                "content": item["result"]
            }
            content.append(data)
        message_list.append({
            "role": "user",
            "content" : content 
        })
        final_response = claude_client.messages.create(
            model = "claude-sonnet-4-6",
            max_tokens = 1024,
            tools = tool_description,
            messages = message_list
        )
        tool_use_status = final_response.stop_reason
    
    print(final_response.content)


call_anthropic("who won the last F1 race")
