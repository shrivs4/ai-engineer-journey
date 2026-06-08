profile = {
    "name": "Shriyam",
    "role": "Forward Deployed Engineer",
    "experience": 10,
    "skills": ["React", "Next.js", "Python", "SQL", "Docker", "Kubernetes"]
}

def calculateExp(exp):
    if exp < 2:
        return 'Junior'
    elif exp < 5:
        return 'Mid'
    elif exp < 10:
        return 'Senior'
    else:
        return "Staff/ Principal"
    

level = calculateExp(10)
# print(level)

def describe_engineer(name, year, role):
    level = calculateExp(year)
    return f"{name} is a {level} {role} with {year} years of experience"

summary = describe_engineer('Shriyam', 10, 'Forward Deployed Engineer')
# print(summary)

def get_skill(profile,index):
    try:
        return profile["skills"][index]
    except IndexError:
        return "Skill not found"

# print(get_skill(profile,0))
# print(get_skill(profile,10))

def analyze_profile(profile):
    level = calculateExp(profile['experience'])
    skill_count = len(profile['skills'])
    return {
        "name": profile["name"],
        "level": level,
        "skill_count": skill_count,
        "top_skill": profile["skills"][0],
        "summary": f"{profile['name']} is a {level} engineer with {skill_count} skills"
    }

print(analyze_profile(profile))