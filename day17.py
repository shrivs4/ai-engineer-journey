from pypdf import PdfReader
from openai import OpenAI
from anthropic import Anthropic
from dotenv import load_dotenv
import chromadb
import re

load_dotenv()
openai_client = OpenAI()
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

allChunks = "\n\n".join([f"[{i}] {chunk}" for i,chunk in enumerate(chunks)])

prompt = f"""refer this chunks from phone spec: {allChunks}
    Question: Does this phone work well with AI assistants?
    which chunk is more relevant to answer the question
"""

response = claude_client.messages.create(
    model = "claude-sonnet-4-6",
    max_tokens = 200,
    messages = [{
        "role" : "user",
        "content": prompt 
    }]
)

print(response.content[0].text)