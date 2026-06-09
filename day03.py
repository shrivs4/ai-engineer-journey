import json


profile = {
    "name": "Shriyam",
    "role": "Forward Deployed Engineer",
    "experience": 10,
    "skills": ["React", "Next.js", "Python", "SQL", "Docker", "Kubernetes"]
}

with open("profile.json", "w") as f:
    json.dump(profile,f,indent=2)

# print("file written!")

with open("profile.json","r") as f:
    load_profile = json.load(f)

print(load_profile)
print(load_profile["name"])
print(load_profile["skills"])

load_profile["skills"].append('LangChain')
load_profile["target_role"] = "Forward Deployed Engineer at Anthropic"

with open("profile.json", "w") as f:
    json.dump(load_profile, f, indent=2)

print('Updated')
print(load_profile)