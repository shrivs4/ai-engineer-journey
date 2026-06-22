import lzma
from pypdf import PdfReader
from openai import OpenAI
from anthropic import Anthropic
from dotenv import load_dotenv
import cohere
import chromadb
from time import perf_counter
import re

load_dotenv()
openai_client = OpenAI()
claude_client = Anthropic()
chroma_client = chromadb.Client()
cohere_client = cohere.ClientV2()


reader = PdfReader("documents/Samsung_m.pdf")

page1_text = reader.pages[0].extract_text()

# def chunk_by_size(text, chunk_size = 100,overlap=20):
#     chunks = []
#     step = chunk_size - overlap
#     for i in range (0, len(text), step):
#         chunk = text[i:i+chunk_size]
#         chunks.append(chunk)
#     return chunks

clean_text = page1_text.replace("\n"," ")
# chunks = chunk_by_size(clean_text,100,20)

sentences = re.split(r'(?<=[.!?])\s+', clean_text)


chunks = [s.strip() for s in sentences if s.strip()]

question = "Does this phone work well with AI assistants?"

start = perf_counter()
response = cohere_client.rerank(
    model="rerank-v3.5",
    query = question,
    documents = chunks
)
end = perf_counter()
print(end - start)

for result in response.results:
    print(f"chunk {chunks[result.index]} score {result.relevance_score}")