from pypdf import PdfReader
from openai import OpenAI
from anthropic import Anthropic
from dotenv import load_dotenv
import chromadb
import re

load_dotenv()
open_ai_client = OpenAI()
claude_client = Anthropic()
chroma_client = chromadb.Client()

reader = PdfReader("documents/Samsung_m.pdf")

page1_text = reader.pages[0].extract_text()

def chunk_by_size(text, chunk_size = 100,overlap=20):
    chunks = []
    step = chunk_size - overlap
    for i in range (0, len(text), step):
        chunk = text[i:i+chunk_size]
        chunks.append(chunk)
    return chunks

clean_text = page1_text.replace("\n"," ")
chunks = chunk_by_size(clean_text,100,20)

# for i, chunk in enumerate(chunks):
#     print(f'--- Chunk {i} ({len(chunk)} chars)')
#     print(chunk)
#     print()

for i, chunk in enumerate(chunks):
    if "Gemini" in chunk:
        print(f"Chunk {i}: {chunk}")

collection = chroma_client.create_collection(name="zfold7_v2")

ids = [f"chunk{i}" for i in range(len(chunks))]

collection.add(documents = chunks, ids = ids)

results = collection.query(
    query_texts=["Does this phone work well with AI assistants?"],
    n_results = 2
)

# print(results['documents'])