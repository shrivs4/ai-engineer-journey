from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, START, END


class AgentState(TypedDict):
    messages: str

def first_node(state: AgentState):
    new_message = state["messages"] + 'This is node one'
    print(new_message)
    return {
        "messages": new_message
    }

def second_node(state: AgentState):
    new_message = state["messages"] + 'This is node two'
    print(new_message)
    return {
        "messages": new_message
    }

graph = StateGraph(AgentState)

graph.add_node("first", first_node)
graph.add_node("second", second_node)

graph.add_edge(START, "first")
graph.add_edge("first", "second")
graph.add_edge("second", END)


new_graph = graph.compile()

new_graph.invoke({"messages": "Hello, this is the initial message."})