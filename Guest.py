from datetime import datetime

class Guest:
    def __init__(self, Name, FamilyName, Car, controlboard,
                 CarRotationManager, ID=0, linkedplatform=None,Start=0):  # --Initializing Guest credentials/info---
        self.Name = Name
        self.FamilyName = FamilyName
        self.Car = Car
        self.controlboard = controlboard
        self.CarRotationManager = CarRotationManager
        if ID == 0: # In this case, the guest would be a new guest, so when we register him as a guest we don't give him an ID, and we ask the controlboard to generate the ID
            self.uniqueID = controlboard.set_id()  # ----calling controlboard class to set ID---unique ID given by control board/decision engine
        else: # In this case, the guest would have already parked before and he would already have an ID, so instead of generating a new ID we just give him his old one
            self.uniqueID = ID
        self.parked = False # Boolean variable which indicates if guest is parked or not
        self.linkedplatform = None # Variable containing the platform where the guest's car is parked
        self.Start=Start # This is the time when the guest parks

    def parked_and_linkedplatform_value(self): # This function checks if the guest is parked and sets the values of linkedplatform and parked accordingly
        (boolean, linkedplatform) = self.CarRotationManager.check_if_guest_parked(self)
        if boolean == True:
            self.parked = True
            self.linkedplatform = linkedplatform
        else:
            self.parked = False
            self.linkedplatform = None

    def request_car(self):  # Function that releases the car if it is parked
        self.parked_and_linkedplatform_value()
        if self.parked == False:
            print("Your car is not parked!\n")
            return
        pos = self.CarRotationManager.get_platform_position(self) # Get the car's current position in the parking
        if (pos == -1):
            print("Your car is not parked!\n")
            return
        self.CarRotationManager.return_platform_to_base(pos) # Move the car to the base position
        self.CarRotationManager.release_car(self.linkedplatform) # Release the car
        self.parked = False
        self.CarRotationManager.occupiedPlatforms = self.CarRotationManager.occupiedPlatforms - 1
        print("Your " + self.Car.model + " has been released.")
        print("Have a great day " + self.Name + "!\n")
        self.controlboard.remove_guest_from_file(self) # We remove the guest from the file once his car is not parked anymore

    def park_car(self): # Function that parks the guest's car if it's not already parked
        self.parked_and_linkedplatform_value()
        if (self.parked == True):
            print("Your car is already parked!\n")
            return
        platform = self.CarRotationManager.return_empty_platform()  # FOUND CLOSEST EMPTY PLATFORM
        if (platform == None):
            return -1  # PARKING IS FULL
        self.CarRotationManager.return_platform_to_base(platform.Position)
        platform.link(self)  # NOW USER'S CAR IS PARKED ON BASE PLATFORM
        self.linkedplatform = platform
        self.parked = True
        self.CarRotationManager.occupiedPlatforms = self.CarRotationManager.occupiedPlatforms + 1
        print("Your " + self.Car.model + " has been parked!\n")
        now = datetime.now() # Get the current time, i.e when the user parks his car
        array = str(now).split()
        string_into_file = array[0] + "@" + array[1]
        self.controlboard.add_guest_to_file(self,string_into_file) # Add the current time (when the user parked) next to his information in the guest file
        self.Start=string_into_file








