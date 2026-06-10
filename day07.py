class Engineer:
    def __init__(self,name, experience):
        self.name = name
        self.experience = experience
        self.skill = []
    
    def decribe(self):
        print(f"{self.name} has {self.experience} years")
    
    def add_skill(self,skill):
        self.skill.append(skill)

    def show_skill(self):
        print(self.skill)    

me = Engineer('Shriyam', 10)

me.decribe()
me.add_skill('React')
me.add_skill('Python')
me.show_skill()

    
    
