import json
from dotenv import load_dotenv 
from anthropic import Anthropic
import os

load_dotenv()
client = Anthropic(api_key = os.getenv("ANTHROPIC_API_KEY"))

with open("engineers.json","r") as f:
    profileList = json.load(f)

def askClaude(profile):
    content = f"Profile: {profile} Question: In one line, what AI Engineering role suits this person best and why?"
    response = client.messages.create(
        model = "claude-sonnet-4-6",
        max_tokens = 1024,
        messages=[
            {"role":"user","content":content,}
        ]
    )

    return response.content[0].text

Analysis = {}

for profile in profileList:
    profile_analysis = askClaude(profile)
    Analysis[profile["name"]] = profile_analysis

with open("recommendations.json","w") as f:
    json.dump(Analysis,f,indent=2)
    
