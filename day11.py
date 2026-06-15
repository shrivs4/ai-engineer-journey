from anthropic import Anthropic
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = Anthropic()
openai_client = OpenAI()

# response = client.messages.count_tokens(
#     model = "claude-sonnet-4-6",
#     messages = [
#         { "role": "user", "content": "Hello Shriyam, how are you doing today?" }
#     ]
# )

# print(f"Token count: {response.input_tokens}")

response = openai_client.embeddings.create(
    model = "text-embedding-3-small",
    input = ["I love dogs", "I adore puppies", "Tax filling 2024"]
)

# for i, embedding in enumerate(response.data):
#     print(f"Text {i}: {len(embedding.embedding)} dimensions")
#     print(f"First 5 values: {embedding.embedding[:5]}")
#     print()

def cosine_similarity(a,b):
    dot_product = sum(x * y for x, y in zip(a,b))
    magnitude_a = sum(x ** 2 for x in a) ** 0.5
    magnitude_b = sum(x ** 2 for x in b) ** 0.5
    return dot_product/ (magnitude_a * magnitude_b)

vec0 = response.data[0].embedding  # "I love dogs"
vec1 = response.data[1].embedding  # "I adore puppies"
vec2 = response.data[2].embedding  # "Tax filing 2024"

print(cosine_similarity(vec0, vec1))  # expect: high
print(cosine_similarity(vec0, vec2)) 