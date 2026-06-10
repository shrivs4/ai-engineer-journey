import requests
import json

with open("users_to_fetch.json","r") as f:
    lst = json.load(f)

def fetchUser(id):
    try:
        response = requests.get(f"https://jsonplaceholder.typicode.com/users/{id}")
        if response.status_code == 200:
            data = response.json()
            return {
                "Name": data["name"],
                "Email": data["email"],
                "City": data["address"]["city"]     
            }
        else:
            return {
                "Name": "",
                "Email": "",
                "City": ""     
        }
    except Exception as e:
        return f"Something went wrong {e}"


userData = []

for id in lst:
    userData.append(fetchUser(id))

with open("fetched_users.json","w") as f:
    json.dump(userData,f,indent=2)

print(f"Fetched {len(userData)} users successfully")
print("Saved to fetched_users.json")