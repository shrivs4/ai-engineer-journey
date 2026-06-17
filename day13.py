import chromadb
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()
client = Anthropic()

chroma_client = chromadb.Client()
collection = chroma_client.create_collection(name="hr_policy")

chunks = [
    "Employees get 12 sick days per year",
    "The office is open from 9am to 6pm Monday to Friday",
    "Remote work is allowed up to 2 days per week",
    "The annual team offsite happens in October",
    "Employees can expense up to 2000 rupees for internet reimbursement monthly"
]

collection.add(
    documents = chunks,
    ids=["doc1", "doc2", "doc3", "doc4", "doc5"]
)

results = collection.query(
    query_texts = ["What's the policy if I'm unwell and need time off?"],
    n_results = 2
)

reterived_chunks = results['documents'][0][0]

prompt = f""" Answer the question using only this context:
{reterived_chunks}
Question: What's the policy if I'm unwell and need timeoff?
"""

response = client.messages.create(
    model = "claude-sonnet-4-6",
    max_tokens = 200,
    messages = [{"role":"user","content":prompt}]
)

print(response.content[0].text)