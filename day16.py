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

# for i, chunk in enumerate(chunks):
#     print(f'--- Chunk {i} ({len(chunk)} chars)')
#     print(chunk)
#     print()


collection = chroma_client.create_collection(name="zfold7_v2")

ids = [f"chunk{i}" for i in range(len(chunks))]

collection.add(documents = chunks, ids = ids)

results = collection.query(
    query_texts=["Does this phone work well with AI assistants?"],
    n_results = 2
)

question_embedding = openai_client.embeddings.create(
    model = "text-embedding-3-small",
    input = ["Does this phone work well with AI assistants?"]
).data[0].embedding

chunk0_embedding = openai_client.embeddings.create(
    model="text-embedding-3-small",
    input=[chunks[0]]
).data[0].embedding

chunk3_embedding = openai_client.embeddings.create(
    model="text-embedding-3-small",
    input=[chunks[3]]
).data[0].embedding

def cosine_similarity(a,b):
    dot_product = sum(x * y for x,y in zip(a,b))
    magnitude_a = sum(x ** 2 for x in a) ** 0.5
    magnitude_b = sum(x ** 2 for x in b) ** 0.5
    return dot_product / (magnitude_a * magnitude_b)

print("chunk0 similarity:", cosine_similarity(question_embedding, chunk0_embedding))
print("chunk3 similarity:", cosine_similarity(question_embedding, chunk3_embedding))

# print(results['documents'])