from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, START,END
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph.message import add_messages
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

class AgentState(TypedDict):
    messages: Annotated[list, add_messages]

memory = MemorySaver()
client = Anthropic()

def node_one(state: AgentState):
    converted = []
    for m in state['messages']:
        role = "user" if m.type == "human" else "assistant"
        converted.append({"role": role, "content": m.content})
    response = client.messages.create(
        model = "claude-sonnet-4-6",
        max_tokens = 1024,
        messages = converted
    )
    print(response.content)
    return {"messages": [{"role": "assistant", "content": response.content[0].text}]}

graph = StateGraph(AgentState)

graph.add_node('node_one',node_one)
graph.add_edge(START,'node_one')
graph.add_edge('node_one',END)

new_graph = graph.compile(checkpointer = memory)

config = {"configurable":{"thread_id":"chat-1"}}

new_graph.invoke(
    {"messages":
     [{"role":"user","content":"I am starting as Jr Developer"}]
     }, config)

new_graph.invoke(
    {"messages":
     [{"role":"user","content":"What did I say my starting role was?"}]
     }, config)