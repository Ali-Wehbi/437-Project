from datetime import datetime

class RegisteredUser:
    def __init__(self, Name, FamilyName, Car, Username, Password, BankAccountNumber, controlboard, CarRotationManager,
                 NumberOfVisits=0,Start=0):  # --Intitializing credentials/info--
        self.Name = Name
        self.FamilyName = FamilyName
        self.Car = Car
        self.Username = Username
        self.Password = Password
        self.BankAccountNumber = BankAccountNumber
        self.NumberOfVisits = NumberOfVisits
        self.controlboard = controlboard
        self.CarRotationManager = CarRotationManager
        self.linkedplatform = None # Variable containing the platform where the user's car is parked
        self.parked = False # Boolean variable which indicates if user is parked or not
        self.Start=Start # This is the time when the user parks
    def parked_and_linkedplatform_value(self): # This function checks if the user is parked and sets the values of linkedplatform and parked accordingly
        (boolean, linkedplatform) = self.CarRotationManager.check_if_user_parked(self)
        if boolean == True:
            self.parked = True
            self.linkedplatform = linkedplatform
        else:
            self.parked = False
            self.linkedplatform = None

    def check_car_location(
            self):  # Determines the location of the user's car (Platform name and Platform level that the car sits on)
        self.parked_and_linkedplatform_value()
        if self.parked == False:
            print("Your car is not parked!\n")
            return
        name = self.CarRotationManager.get_platform_name(self)
        level = self.CarRotationManager.get_platform_level(self)
        if level == -1:
            print("Your Car " + self.Car.model + " is not in the Parking\n")
        else:
            print("Your Car " + self.Car.model + " is on Platform " + name + " and it's on level " + str(level) + "\n")

    def __str__(self):  # prints information for a Registered User
        return (
                "Full name: " + self.Name + " " + self.FamilyName + "\n" + "Car Model: " + self.Car.model + "\n" + "Username: " + self.Username + "\n" + "Number of Visits: " + str(
            self.NumberOfVisits))

    def request_car(self):   # Function that releases the car if it is parked
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
        self.controlboard.add_start_time(self,'0')

    def park_car(self): # Function that parks the user's car if it's not already parked
        self.parked_and_linkedplatform_value()
        if self.parked == True:
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
        self.controlboard.increment_nb_visits(self)
        print("Your " + self.Car.model + " has been parked!\n")
        now = datetime.now() # Get the current time, i.e when the user parks
        array = str(now).split()
        string_into_file = array[0] + "@" + array[1]
        self.controlboard.add_start_time(self,string_into_file) # Add this time (when the car is parked) next to this user's information in the file
