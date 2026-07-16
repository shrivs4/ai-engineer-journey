from anthropic import Anthropic
from dotenv import load_dotenv
import os
from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated
from langgraph.graph.message import add_messages



load_dotenv()
client = Anthropic()

class AgentState(TypedDict):
    messages : Annotated[list, add_messages]


def claude_conversion(message):
    formated_list = []
    for m in message:
        role = "user" if m.type == "human" else "assistant"
        formated_list.append({"role": role, "content": m.content})
    return formated_list

def ask_claude(state: AgentState):
    message_list = claude_conversion(state['messages'])
    fullText = ""
    with client.messages.stream(
        model = "claude-sonnet-4-6",
        max_tokens = 1024,
        messages=message_list
    ) as stream:
        print(stream.text_stream,'team')
        for text in stream.text_stream:
            fullText += text
            print(text, end="",flush=True)
    
    return {
        "messages": [{"role":"assistant", "content": fullText}]
    }

graph = StateGraph(AgentState)

graph.add_node("ask_claude", ask_claude)

graph.add_edge(START, "ask_claude")
graph.add_edge("ask_claude", END)

newGraph = graph.compile()

newGraph.invoke(
    {"messages": [{"role": "user", "content": "What is a Forward Deployed engineer? Explain in 3 lines."}]}
    )




