from pypdf import PdfReader
import re
import chromadb
from dotenv import load_dotenv
from anthropic import Anthropic
from tavily import TavilyClient
import json
import os
from typing import TypedDict, Any
from langgraph.graph import StateGraph,START,END

class AgentState(TypedDict):
    messages : list
    last_response: Any


load_dotenv()

client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
claude_client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

chroma_client = chromadb.Client()

collection = chroma_client.create_collection(name = "zfold7_specs")

reader = PdfReader("documents/Samsung_m.pdf")

full_text = ''

for page in reader.pages:
    page_text = page.extract_text()
    full_text += page_text

def chunk_by_size(text, chunk_size, overlap):
    chuncks = []
    step = chunk_size - overlap
    for i in range(0, len(text),step):
        chunk = text[i: i+chunk_size]
        chuncks.append(chunk)
    return chuncks

chunks = chunk_by_size(full_text,100,20)

ids = [f"chunk {i}" for i in range(len(chunks))]

collection.add(documents = chunks, ids = ids)

def search_document(query):
    result = collection.query(
        query_texts = query,
        n_results = 4
    )
    return result["documents"][0]

def search_web(query):
    response = client.search(query)
    result_data = []
    for result in response["results"]:
        result_data.append({
            "title":result["title"],
            "content": result["content"]
        })
    return result_data

required_tools = {
    "search_document": search_document,
    "search_web": search_web
}

tool_description = [
    {
        "name": "search_web",
        "description": "Search the internet for current, real-time, or recent information — use this when the answer requires up-to-date facts not in your training data.",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "This could be any question eg: Who is f1 winner?"
                }
            },
            "required": ["query"]
        }
    },
    {
        "name": "search_document",
        "description": "Search the Samsung Galaxy Z Fold7 product specification document for information about hardware specs, dimensions, battery, cameras, display, and features.",
        "input_schema": {
            "type": "object",
            "properties":{
                "query": {
                    "type": "string",
                    "description": "This could be any question related to samsung specification",
                }
            },
            "required": ["query"]
        }
    }
]

def ask_claude(state: AgentState):
    response = claude_client.messages.create(
        model = "claude-sonnet-4-6",
        max_tokens = 1024,
        tools = tool_description,
        messages = state["messages"]
    )
    new_messages = state['messages'] + [{"role": "assistant", "content": response.content}]
    return {
    "messages": new_messages,
    "last_response": response
    }

def run_tool(state: AgentState) -> AgentState:
    results = []
    for block in state["last_response"].content:
        if block.type == "tool_use":
            tool = required_tools[block.name]
            result = tool(**block.input)
            results.append({
                "id": block.id,
                "result": json.dumps(result)
            })
    
    content = []

    for item in results:
            data = {
                "type": "tool_result",
                "tool_use_id": item["id"],
                "content": item["result"]
            }
            content.append(data)
    new_messages = state["messages"] + [{"role": "user", "content": content}]

    return {
        "messages": new_messages,
        "last_response": state["last_response"]
    }



def router(state: AgentState):
    for block in state["last_response"].content:
        if block.type == "tool_use":
            return "run_tool"
    return END

graph_builder = StateGraph(AgentState)

graph_builder.add_node("ask_claude", ask_claude)
graph_builder.add_node("run_tool",run_tool)


graph_builder.add_edge(START,"ask_claude")
graph_builder.add_conditional_edges("ask_claude",router)

graph_builder.add_edge("run_tool","ask_claude")

graph = graph_builder.compile()

# initial_state = {
#     "messages": [{"role": "user", "content": "What is the battery capacity of Samsung Z Fold7?"}],
#     "last_response": None
# }

initial_state = {
    "messages": [{"role": "user", "content": "Who won the last F1 race?"}],
    "last_response": None
}

result = graph.invoke(initial_state)
print(result["messages"][-1])












