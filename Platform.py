class Platform: #A platform is either “Empty” or has a Car(linked to a person)
    def __init__(self, Position, name):
        self.Position = Position
        self.name = name
        self.linkedperson = "NULL"

    def __str__(self):  # prints the platform name, and the info of the Car linked to it (if not empty)
        if self.is_empty():
            return "Platform " + (self.name) + " is at position " + str(self.Position) + " and it's empty.\n"
        statement = "Platform " + (self.name) + " is at position " + str(
            self.Position) + ", and on it we have " + self.linkedperson.Name + " " + self.linkedperson.Car.OwnerFamilyName + "'s " + self.linkedperson.Car.model + "\n"
        return statement

    def link(self, person):
        self.linkedperson = person

    def is_empty(self):
        if self.linkedperson == "NULL":  # ---empty platform---
            # print("Platform is empty")
            return True
        else:  # ---platform nonempty/linked to a person---
            return False