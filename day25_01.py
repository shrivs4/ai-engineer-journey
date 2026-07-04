from typing import TypedDict
from langgraph.graph import StateGraph, START, END


class AgentState(TypedDict):
    number: int
    result: str

def check_number(state: AgentState) -> AgentState:
    print(f"Checking number: {state['number']}")
    return state

def handle_even(state: AgentState) -> AgentState:
    print("Handling even branch")
    return {"number": state["number"], 
            "result": "It was even"}

def handle_odd(state:AgentState) -> AgentState:
    print("Handling odd branch")
    return {
        "number": state["number"],
        "result": "it was odd"
    }

def router(state: AgentState) -> str:
    if state["number"] % 2 ==0:
        return "even_node"
    else:
        return "odd_node"

graph_builder = StateGraph(AgentState)

graph_builder.add_node("check",check_number)
graph_builder.add_node("even_node",handle_even)
graph_builder.add_node("odd_node",handle_odd)

graph_builder.add_edge(START,"check")

graph_builder.add_conditional_edges("check",router)

graph_builder.add_edge("even_node", END)
graph_builder.add_edge("odd_node", END)

graph = graph_builder.compile()

print(graph.invoke({"number": 4, "result": ""}))
print("---")
print(graph.invoke({"number": 7, "result": ""}))
