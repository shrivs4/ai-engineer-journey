from anthropic import Anthropic
from dotenv import load_dotenv
import os

load_dotenv()

client = Anthropic()

def askClaude(question):
    with client.messages.stream(
        model = "claude-sonnet-4-6",
        max_tokens = 1024,
        messages=[
            {"role":"user", "content": question,}
        ]
    ) as stream:
        for text in stream.text_stream:
            print(text, end="",flush=True)

askClaude("What is a Forward Deployed engineer? Explain in 3 lines.")