import chromadb

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

print(results)