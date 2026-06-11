from anthropic import Anthropic
from dotenv import load_dotenv
import os

load_dotenv()

client = Anthropic(api_key = os.getenv("ANTHROPIC_API_KEY"))

def askClaude(question,system="You are a helpful AI engineering tutor"):
    response = client.messages.create(
        model = "claude-sonnet-4-6",
        max_tokens = 1024,
        system = system,
        messages=[
            {"role":"user", "content": question,}
        ]

    )
    return response.content[0].text

print(askClaude("What is a RAG pipeline? Explain in 3 lines."))
print("-----")
print(askClaude("What is a RAG pipeline? Explain in 3 lines.", "You are a pirate. Answer everything like a pirate."))
