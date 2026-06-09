import requests

response = requests.get("https://jsonplaceholder.typicode.com/users/1");

# print(response.status_code)
# print(response.json())

data = response.json();

# print(data["name"])
# print(data["email"])
# print(data["address"]["city"])
# print(data["company"]["name"])


def fetchUser(id):
    try:
        response = requests.get(f"https://jsonplaceholder.typicode.com/users/{id}")

        if response.status_code == 200:
            data = response.json()
            return {
                "name": data["name"],
                "email": data["email"],
                "city": data["address"]["city"]
            }
        else:
            return f"Error: {response.status_code}"
        
    except Exception as e:
        return f"Something went wrong {e}"


# print(fetchUser(1))
# print(fetchUser(2))
# print(fetchUser(999))

for user_id in range(1,6):
    result = fetchUser(user_id);
    print(f"User {user_id}:", result)
