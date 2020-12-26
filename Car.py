class Car:
    def __init__(self, model, platenumber, OwnerName="NULL", OwnerFamilyName="NULL"):  # ---Initializing car info---
        self.model = model
        self.platenumber = platenumber
        self.OwnerName = OwnerName
        self.OwnerFamilyName = OwnerFamilyName

    def __str__(self): # Printing car info
        return ("Car Model: " + self.model + "\n" + "Plate Number: " + str(
            self.platenumber) + "\n" + "Car Owner: " + self.OwnerName + " " + self.OwnerFamilyName)