from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

client = Anthropic()

app = FastAPI()


class Question(BaseModel):
    question: str

@app.get('/')
def home():
    return {"message": "hello"}

@app.post('/ask')
def ask(body: Question):
    answer = ask_claude(body.question)
    return {
        "answer": answer
    }

@app.post('/ask-stream')
def ask_stream(body: Question):
    return StreamingResponse(generate(body.question))

def ask_claude(question: str):
    response = client.messages.create(
        model = 'claude-sonnet-4-6',
        max_tokens = 1024,
        messages = [
            {"role":"user","content":question}
        ]
    )
    return response.content[0].text

def generate(question: str):
    with client.messages.stream(
        model = "claude-sonnet-4-6",
        max_tokens = 1024,
        messages = [
            {"role":"user","content": question}
        ]
    ) as stream:
        for text in stream.text_stream:
            yield text

