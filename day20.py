from anthropic import Anthropic
from dotenv import load_dotenv
import os

load_dotenv()

client = Anthropic(api_key = os.getenv("ANTHROPIC_API_KEY"))

def calculate(expression):
    return str(eval(expression))

toolDescription = [
    {"name": "calculate",
     "description": "This function will take string number expression eg: 2*2 or 2+3 and calculate and give us the response",
     "input_schema": {
         "type": "object",
         "properties": {
             "expression": {
                 "type": "string",
                 "description": "this experession will be desired calculation like 2*2 or 3/4 or 3+3"
             },

         },
         "required": ["expression"]
     }
     }
]

available_tools = {
    "calculate": calculate
}

def askClaude():
    response = client.messages.create(
        model = "claude-sonnet-4-6",
        max_tokens = 1024,
        tools = toolDescription,
        messages = [{"role":"user","content": "what is 847 * 936, then divide the result by 4?"}]
    )
    tool_call = None
    messages_to_give = [{"role":"user","content": "what is 847 * 936, then divide the result by 4?"}]
    stop_reason = response.stop_reason
    final_response = response
    while stop_reason == "tool_use":
        for block in final_response.content:
            if block.type == "tool_use":
                tool_call = block
        tool_function = available_tools[tool_call.name]
        result = tool_function(**tool_call.input)
        messages_to_give.append({"role": "assistant", "content": final_response.content})
        messages_to_give.append({"role": "user", "content": [
                        {
                            "type": "tool_result",
                            "tool_use_id": tool_call.id,
                            "content" : result 
                        }
                    ]})
        final_response = client.messages.create(
        model = "claude-sonnet-4-6",
        max_tokens = 1024,
        tools = toolDescription,
        messages = messages_to_give
        )
        stop_reason = final_response.stop_reason
    print(final_response.content)

result = askClaude()






    



