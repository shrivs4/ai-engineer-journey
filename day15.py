from pypdf import PdfReader
import re
import chromadb
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()
client = Anthropic();

chroma_client = chromadb.Client()

collection = chroma_client.create_collection(name="zfold7_specs")

reader = PdfReader("documents/Samsung_m.pdf")

# full_text = ""

# for page in reader.pages:
#     full_text += page.extract_text() + "\n"

page1_text = reader.pages[0].extract_text()
clean_text =  page1_text.replace("\n"," ")

sentences = re.split(r'(?<=[.!?])\s+', clean_text)


chunks = [s.strip() for s in sentences if s.strip()]

ids = [f"chunk{i}" for i in range(len(chunks))]

collection.add(
    documents = chunks,
    ids = ids
)

results = collection.query(
    query_texts = ["Does this phone work well with AI assistants?"],
    n_results = 2
)

retrieved_chunks = "\n".join(results['documents'][0])

prompt = f"""Answer the question using only this context
 {retrieved_chunks}
    Question: Does this phone work well with AI assistants? """

response = client.messages.create(
    model = "claude-sonnet-4-6",
    max_tokens = 200,
    messages = [{"role":"user", "content": prompt}]
)

print(response.content[0].text)


