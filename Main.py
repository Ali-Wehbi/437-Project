from CarRotationManager import CarRotationManager
from ControlBoard import ControlBoard

#MAIN
#For testing purposes, we're going to create 5 parkings, each containing 12 platforms (slots for parking)
Parking1 = CarRotationManager('A', 12) #Name: A, Number of Platforms: 12
Parking2 = CarRotationManager('B', 12)
Parking3 = CarRotationManager('C', 12)
Parking4 = CarRotationManager('D', 12)
Parking5 = CarRotationManager('E', 12)
ArrayOfParkings = [Parking1, Parking2, Parking3, Parking4, Parking5]

#Each Parking is associated with a controlboard next to it.
controlboard1 = ControlBoard(Parking1, ArrayOfParkings)
controlboard2 = ControlBoard(Parking2, ArrayOfParkings)
controlboard3 = ControlBoard(Parking3, ArrayOfParkings)
controlboard4 = ControlBoard(Parking4, ArrayOfParkings)
controlboard5 = ControlBoard(Parking5, ArrayOfParkings)
ArrayOfCBs=[controlboard1,controlboard2,controlboard3,controlboard4,controlboard5]

#In real life, a person will manually choose his/her preferred parking space, get
#to the parking's controlboard and enter their credentials in order to park
#Here, for testing purposes, we will allow users to choose their parking before hand,
#In order to show them which parkings are full, and which are not.
#After choosing the parking, the user will then interact with the controlboard, to park or release their car.
while True:
    #Printing Parkings' info, so that a user chooses which parking he/she wants to visit.
    for i in range(len(ArrayOfCBs)):
        ArrayOfParkings[i].parking_info()
    print("Choose between the " + str(len(ArrayOfCBs)) + " parkings by entering their corresponding name:")
    Pkng=input()
    if Pkng.upper()=="A":
        controlboard1.welcome()
    elif Pkng.upper()=="B":
        controlboard2.welcome()
    elif Pkng.upper()=="C":
        controlboard3.welcome()
    elif Pkng.upper()=="D":
        controlboard4.welcome()
    elif Pkng.upper()=="E":
        controlboard5.welcome()
    else:
        print("Invalid input")
        print("\n")
        continue