from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph.message import add_messages
from anthropic import Anthropic
from dotenv import load_dotenv


load_dotenv()
client = Anthropic()

memory = MemorySaver()

class AgentState(TypedDict):
    messages: Annotated[list, add_messages]
    next: str

def claude_conversion(message):
    formated_list = []
    for m in message:
        role = "user" if m.type == "human" else "assistant"
        formated_list.append({"role": role, "content": m.content})
    return formated_list

def callClaude(messages_list):
    response = client.messages.create(
        model = "claude-sonnet-4-6",
        max_tokens = 1024,
        messages = messages_list
    )
    return response

def supervisor(state: AgentState):
    supervisor_prompt = """You are a supervisor managing two workers:
        - researcher: uses web search for current, real-time, or general knowledge questions
        - doc_expert: answers questions about the Samsung Galaxy Z Fold7 (specs, battery, display, cameras)

        Based on the conversation, reply with ONLY ONE WORD - who should act next:
        - 'researcher' if it needs web search
        - 'doc_expert' if it's about the Samsung Galaxy Z Fold7
        - 'FINISH' if the question has already been fully answered
        Reply with ONLY that one word, nothing else."""
    messages_list = claude_conversion(state["messages"])
    messages_list += [{"role": "user", "content": supervisor_prompt}]
    response = callClaude(messages_list)
    decision = response.content[0].text.strip()
    print(state)
    return {
        "next": decision
    }


def researcher(state: AgentState):
    researcher_prompt = "You are a research specialist. Answer the user's question clearly and concisely."
    message_list=claude_conversion(state["messages"])
    message_list+= [{"role":"user","content":researcher_prompt}]
    response = callClaude(message_list)
    return {
        "messages": [{"role": "assistant", "content": response.content[0].text}]
    }

def doc_expert(state: AgentState):
    doc_expert_prompt = "You are a Samsung Galaxy Z Fold7 specialist. Answer questions about its specs, battery, display, and cameras."
    message_list =claude_conversion(state['messages'])
    message_list += [{"role":"user","content": doc_expert_prompt}]
    response = callClaude(message_list)
    return {
        "messages": [{"role":"assistant", "content": response.content[0].text}]
    }

def router(state: AgentState):
    current = state["next"]
    if current == "researcher":
        return "researcher"
    elif current == "doc_expert":
        return "doc_expert"
    else:
        return END
    
graph = StateGraph(AgentState)

graph.add_node("supervisor",supervisor)
graph.add_node("researcher",researcher)
graph.add_node("doc_expert",doc_expert)

graph.add_edge(START,"supervisor")
graph.add_conditional_edges("supervisor",router)
graph.add_edge("researcher","supervisor")
graph.add_edge("doc_expert","supervisor")

new_graph = graph.compile(checkpointer=memory)

config = {"configurable":{"thread_id":"chat-1"},"recursion_limit": 10}

new_graph.invoke(
    {"messages": [{"role": "user", "content": "What is the battery capacity of the Z Fold7?"}]},
    config
)