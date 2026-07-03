from pypdf import PdfReader
import re
import chromadb
from dotenv import load_dotenv
from anthropic import Anthropic
from tavily import TavilyClient
import json
import os

load_dotenv()

client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
claude_client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

chroma_client = chromadb.Client()

collection = chroma_client.create_collection(name= "zfold7_specs")

reader = PdfReader("documents/Samsung_m.pdf")

full_text = ''

for page in reader.pages:
    page_text = page.extract_text()
    full_text += page_text

def chunk_by_size(text, chunck_size = 100, overlap = 20):
    chuncks=[]
    step = chunck_size - overlap
    for i in range(0, len(text), step):
        chunck = text[i:i+chunck_size]
        chuncks.append(chunck)
    return chuncks

clean_text = full_text.replace("\n", " ");

chunks = chunk_by_size(clean_text,100,20)

ids = [f"chunk{i}" for i in range(len(chunks))]

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

def call_anthropic(query):
    response = claude_client.messages.create(
        model = "claude-sonnet-4-6",
        max_tokens = 1024,
        tools = tool_description,
        messages = [{
            "role": "user",
            "content": query
        }]
    )
    final_response = response
    tool_use_status = final_response.stop_reason
    messages_list = [
        {"role":"user",
         "content": query}
    ]
    counter = 0
    while tool_use_status == "tool_use" and counter<10:
        results = []
        for block in final_response.content:
            if(block.type == "tool_use"):
                tool = required_tools[block.name]
                result = tool(**block.input)
                results.append({
                    "id": block.id,
                    "result": json.dumps(result)
                })
        
        messages_list.append({
            "role": "assistant",
            "content": final_response.content
        })
        content = []

        for item in results:
            data = {
                "type": "tool_result",
                "tool_use_id": item["id"],
                "content": item["result"]
            }
            content.append(data)
        messages_list.append({
            "role": "user",
            "content": content
        })

        final_response = claude_client.messages.create(
            model = "claude-sonnet-4-6",
            max_tokens = 1024,
            tools = tool_description,
            messages = messages_list
        )
        counter+=1
        tool_use_status = final_response.stop_reason

    print(final_response.content)







# call_anthropic("How does the Samsung Z Fold7 compare to the latest iPhone Pro Max in terms of battery capacity?")

call_anthropic("does this work with AI assistants")





