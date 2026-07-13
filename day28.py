from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph.message import add_messages
from anthropic import Anthropic
from dotenv import load_dotenv
from tavily import TavilyClient
import json
from pypdf import PdfReader
import chromadb


load_dotenv()
client = Anthropic()
TavilyClient = TavilyClient()

chroma_client = chromadb.Client()

collection = chroma_client.create_collection(name="zfold7_specs")

reader = PdfReader("documents/Samsung_m.pdf")

full_text = ""

for page in reader.pages:
    page_text = page.extract_text()
    full_text += page_text

def chunk_by_size(text, chunk_size=100, overlap=20):
    chunks = []
    step = chunk_size - overlap
    for i in range(0, len(text), step):
        chunk = text[i:i + chunk_size]
        chunks.append(chunk)
    return chunks

chunks = chunk_by_size(full_text)

ids = [f"{chunk_id}" for chunk_id in range(len(chunks))]

collection.add(documents=chunks, ids=ids)

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
        - if doc_expert is already been called and it says is does not have the answer, then the researcher should be called next
        - if the question has already been fully answered, then the process should end

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


def search_web(query):
    response = TavilyClient.search(query)
    result_data = []
    for result in response["results"]:
        result_data.append({"title": result["title"], "content": result["content"]})
    return result_data

def search_document(query):
    result = collection.query(
        query_texts=[query],
        n_results=4
    )
    return result["documents"][0]


def researcher(state: AgentState):
    query = state["messages"][0].content
    search_results = search_web(query)
    prompt = f"You are a research specialist. Answer the user's question clearly and concisely.\n\n {json.dumps(search_results)}"
    message_list=claude_conversion(state["messages"])
    message_list+= [{"role":"user","content":prompt}]
    response = callClaude(message_list)
    return {
        "messages": [{"role": "assistant", "content": response.content[0].text}]
    }

def doc_expert(state: AgentState):
    query = state["messages"][0].content
    doc_results = search_document(query)
    doc_expert_prompt = f"You are a Samsung Galaxy Z Fold7 specialist. Answer questions about its specs, battery, display, and cameras {json.dumps(doc_results)}"
    message_list =claude_conversion(state['messages'])
    message_list += [{"role":"user","content": doc_expert_prompt}]
    response = callClaude(message_list)
    return {
        "messages": [{"role":"assistant", "content": response.content[0].text}]
    }

def router(state: AgentState):
    current = state["next"]
    last_tool = (m.type == "ai" for m in state["messages"])

    if current == "researcher":
        return "researcher"
    elif current == "doc_expert" and last_tool:
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