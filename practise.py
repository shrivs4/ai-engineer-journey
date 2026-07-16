from email import message
from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages


class AgentState(TypedDict):
    messages: Annotated[list, add_messages]
    next: str

def router(state: AgentState):
    if(state['next'] == "researcher"):
        return "researcher" ##this just for example we are not wrtiing niode here 
    else:
        return END

graph = StateGraph(AgentState)

graph.add_conditional_edges('router', router)

new_graph = graph.compile()

new_graph.invoke({
    "messages":[{"role":"user","content":"What is the battery capacity of the Z Fold7?"}]
})