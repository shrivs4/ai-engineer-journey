from typing import TypedDict, Annotated 
from langgraph.graph import StateGraph,START,END
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph.message import add_messages

class AgentState(TypedDict):
    messages: Annotated[list, add_messages]

memory = MemorySaver()

def node_one(state: AgentState)-> AgentState:
    print(state['messages'])
    return {
        "messages": [{"role": "assistant", "content": "message from node one"}] 
    }

graph = StateGraph(AgentState)

graph.add_node('node_one', node_one)

graph.add_edge(START, 'node_one')
graph.add_edge('node_one',END)

new_graph = graph.compile(checkpointer=memory)

config = {"configurable" : {"thread_id": "chat-1"}}

new_graph.invoke({"messages": [{"role": "user", "content": "first"}]}, config)
new_graph.invoke({"messages": [{"role": "user", "content": "second"}]}, config)





