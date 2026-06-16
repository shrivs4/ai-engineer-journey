from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
openai_client = OpenAI()

document = """
Employees get 12 sick days per year.
The office is open from 9am to 6pm Monday to Friday.
Remote work is allowed up to 2 days per week.
The annual team offsite happens in October.
Employees can expense up to 2000 rupees for internet reimbursement monthly.
"""

chunks = [chunk.strip() for chunk in document.split(".") if chunk.strip()]

chunks_embeddings_response = openai_client.embeddings.create(
    model = "text-embedding-3-small",
    input = chunks
)

chunk_vectors = [item.embedding for item in chunks_embeddings_response.data]

question = "What's the policy if I'm unwell and need time off?"

question_embedding_response = openai_client.embeddings.create(
    model = "text-embedding-3-small",
    input = question
)

question_vectors = question_embedding_response.data[0].embedding

def cosine_similarity(a, b):
    dot_product = sum(x * y for x, y in zip(a, b))
    magnitude_a = sum(x ** 2 for x in a) ** 0.5
    magnitude_b = sum(x ** 2 for x in b) ** 0.5
    return dot_product / (magnitude_a * magnitude_b)

best_score = 0
best_chunk = None

for i, chunk_vector in enumerate(chunk_vectors):
    similarity_score = cosine_similarity(chunk_vector,question_vectors)
    if similarity_score > best_score:
        best_score = similarity_score
        best_chunk = chunks[i]

print(best_score)
print(best_chunk)
 