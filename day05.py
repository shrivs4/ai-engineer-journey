from dotenv import load_dotenv
import os

load_dotenv()


with open("notes.txt","w") as f:
    f.write("Day 1 - Variables and functions\n")
    f.write("Day 2 - Error handling\n")
    f.write("Day 3 - JSON\n")
    f.write("Day 4 - API calls\n")

print('Written!')

with open("notes.txt","r") as f:
    content = f.read()


print(content)

name = os.getenv('MY_NAME');
role = os.getenv("TARGET_ROLE");

print(f"Name: {name}")
print(f"Role: {role}")

