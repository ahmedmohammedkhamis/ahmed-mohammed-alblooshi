
class Person:
    def __init__(self, name, number, location, job_title):
        self.name = name
        self.number = number
        self.location = location
        self.job_title = job_title


people = [
    Person("Ahmed", 12345, "Dubai", "Engineer"),
    Person("Ali", 23456, "Abu Dhabi", "Pilot"),
    Person("Omar", 34567, "Al Ain", "Teacher"),
    Person("Sara", 45678, "Sharjah", "Doctor"),
    Person("Mona", 56789, "Ajman", "Manager")
]

with open("people.json", "w") as file:
    file.write("[\n")

    for i, person in enumerate(people):
        file.write("  {\n")
        file.write(f'    "name": "{person.name}",\n')
        file.write(f'    "number": {person.number},\n')
        file.write(f'    "location": "{person.location}",\n')
        file.write(f'    "job_title": "{person.job_title}"\n')
        file.write("  }")

        if i < len(people) - 1:
            file.write(",")

        file.write("\n")

    file.write("]")

print("JSON file created successfully!")
