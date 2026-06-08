# name = 'Shriyam'
# experience = 10
# is_learning = True

# print(name)
# print(experience)
# print(is_learning)

skills = ["React", "Next.js", "Python", "SQL", "Docker", "Kubernetes"]

# print(skills)
# print(skills[0])
# print(len(skills))

profile = {
    "name": "Shriyam",
    "role": "Forward Deployed Engineer",
    "experience": 10,
    "is_learning": True,
    "skills": ["React", "Next.js", "Python", "SQL", "Docker", "Kubernetes"]
}

# print(profile["name"])
# print(profile["role"])
# print(profile["experience"])
# print(profile["skills"])

def introduce (profile):
    print("Name:",profile["name"])
    print("Role:",profile["role"])
    print("Experience",profile["experience"])
    print("Skills",profile["skills"])

# introduce(profile)

print("My Skills")
for skills in profile["skills"]:
    print("-",skills)
