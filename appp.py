class Person:
    def __init__(self, name, age, gender):
        self.name = name
        self.age =age
        self.gender = gender

person = Person("田中花子", 64.435, "男")
print(person.name)