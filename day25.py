from typing import TypedDict
from langgraph.graph import StateGraph, START, END

class AgentState(TypedDict):
    message: str


def node_one(state: AgentState) -> AgentState:
    print("Node 1 running")
    return {
        "message": state["message"]+ "-> touched by node 1"
    }

def node_two(state: AgentState) -> AgentState:
    print("Node 2 running")
    return {
        "message": state["message"]+ "-> touched by node 2"
    }

graph_builder = StateGraph(AgentState)

graph_builder.add_node("first", node_one)
graph_builder.add_node("second", node_two)

graph_builder.add_edge(START, "first")
graph_builder.add_edge("first","second")
graph_builder.add_edge("second",END)

graph = graph_builder.compile()

result = graph.invoke({"message": "hello"})

print(result)