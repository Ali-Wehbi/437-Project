from random import randint
from RegisteredUser import RegisteredUser
from Car import Car
from Guest import Guest
import math
import time
from datetime import datetime

class ControlBoard:
    def __init__(self, CarRotationManager, ArrayOfParkings):
        self.IDcounter = 10000 # We want all the IDs to be in the range of 10000 and above, so we initialize the ID to 10000
        self.CarRotationManager = CarRotationManager
        self.ArrayOfParkings = ArrayOfParkings

    def set_id(self): # To generate a new ID, we take the latest ID that we generated and add a number between 30 and 90 to it (random)
        self.IDcounter = self.IDcounter + randint(30, 90) #the choice of randint was randomly picked by us.
        return self.IDcounter

    def remove_spaces(self, string): # Function to make sure that a string has no spaces, in other words it turns a string into a single word
        string = string.split()           #This function is used to prevent any errors when writing on the user and guest files.
        summa = ''
        for comp in string:
            summa += comp
        return summa

    def register(self): #Function that takes info to create a registered user account; then adds the info into the user file.It returns a registered user.
        Name = input("Name:\n")
        FamilyName = input("family name:\n")
        model = input("car model:\n")
        model = self.remove_spaces(model)
        platenumber = input("plate number:\n")
        car1 = Car(model, platenumber, Name, FamilyName)
        Username = input("username:\n")
        while (self.already_existing_username(Username) == True):  # ---checks if username is already taken---
            print("Username already exists, please choose a different username:\n")
            Username = input("username:\n")
        Password = input("password:\n")
        BankAccountNumber = input("Bank account number:\n")
        print("Welcome " + Name + ", you have been registered as a user!")
        p1 = RegisteredUser(Name, FamilyName, car1, Username, Password, BankAccountNumber, self,self.CarRotationManager,0)  # ---initialize ResgisteredUser---
        self.add_user_to_file(p1) # Adds the user (his information) to the file
        return p1

    def continue_as_guest(self): #Function that takes info to create a guest; then adds the info into the guest file.It returns a new Guest object.
        Name = input("Please enter your name:\n")
        FamilyName = input("Please enter your family name:\n")
        model = input("Please enter your car model:\n")
        model = self.remove_spaces(model)
        platenumber = input("Please enter your car's plate number:\n")
        car1 = Car(model, platenumber, Name, FamilyName)
        p1 = Guest(Name, FamilyName, car1, self, self.CarRotationManager)  # ---initialize guest---
        print("Welcome" + " " + Name + "!")
        print("Your ID number is: " + str(p1.uniqueID))
        print("Remember your ID number, you must enter it back to pick up your car.")
        return p1

    def login(self): # For users who were previously registered, we just log them in using this function. Returns an already registered user.
        username = input("Input the username\n")
        password = input("Input the password\n")
        (userbool, passbool, creds) = self.check_user(username,
                                                      password)  # ---function to check the username and password---
        # Userbool is related to the correctness of the username, passbool is related to the correctness of the password, and creds are the information from the file
        while (userbool != True or passbool != True):
            if (userbool == True and passbool == False):  # ---correct username and wrong password---
                print("Invalid password, Please type the correct password\n")
                password = input("password:\n")
                (userbool, passbool, creds) = self.check_user(username, password)
            elif (userbool == False):  # ---wrong username only---
                print("Incorrect username, please type the correct username and password\n")
                username = input("username:\n")
                password = input("password:\n")
                (userbool, passbool, creds) = self.check_user(username, password)
        print("Login sucessful!\n")
        c1 = Car(creds[2], creds[3], creds[0], creds[1])  # ---CARNB,PLTNB,NAME,FNAME---
        AlreadyRegisteredUser = RegisteredUser(creds[0], creds[1], c1, creds[4], creds[5], creds[6], self,
                                               self.CarRotationManager, creds[7],creds[8])
        return AlreadyRegisteredUser

    def welcome(self):  # ---This function allows the user to register/login/continue as a guest---
        print("Welcome to Parking " + self.CarRotationManager.Name + "!")
        print("To register as a new user, enter 'register'")
        print("To login, enter 'login'")
        print("To continue as a new guest, enter 'guest'")
        print("If you are a guest and you already have an ID, enter 'oldguest'")
        Input = input()
        if Input == "register":  # ---user wants to create an account / takes info as input from him/her---
            p1 = self.register()
            self.user_options(p1)
        elif Input == "login":  # ---user already has an account and wants to login---
            p1 = self.login()
            self.user_options(p1)
        elif Input == "guest":  # ---takes info from the user as input---
            p1 = self.continue_as_guest()
            self.guest_options(p1)
        elif Input == "oldguest":
            print("What's your ID?")
            ID = input()
            p1 = self.retreive_guest(ID)
            if p1 == None:
                print("It looks like you are not an old guest!")
                print("Redirecting you to main page")
                self.welcome()
            print("Welcome back" + " " + p1.Name)
            self.guest_options(p1)
        else:
            print("Invalid Input, redirecting you to main page")
            self.welcome()
            
    def retreive_guest(self, ID): # If a guest parked before and came back to release their car, we need to retrieve their information from the guest file
        f = open('437Guest.txt', 'r')
        line = f.readline()
        while line != '':
            test = line.split()
            if ID == test[4]:
                car1 = Car(test[2], test[3], test[0], test[1])
                p1 = Guest(test[0], test[1], car1, self, self.CarRotationManager,ID,test[5])  # ---initialize guest---
                return p1
            line = f.readline()
        return None

    def check_user(self, username, password):  # ---function to check if username and password are correct---
        namehandle = open("437User.txt")  # ---text file that stores all registered users credentials---
        line = namehandle.readline()
        while line != '':
            test = line.split()
            if test[4] == username and test[5] != password:  # ---correct username but wrong password---
                return (True, False, [])
            elif test[4] == username and test[5] == password:  # ---both username and password are correct---
                return (True, True, test)
            line = namehandle.readline()
        return (False, False, [])  # --incorrect user--

    def already_existing_username(self, Username): # If someone wants to register, this function checks if the name he inputs already exists or not
        namehandle = open("437User.txt")
        line = namehandle.readline()
        while line != '':
            test = line.split()
            if Username == test[4]: # test[4] is the username in the file that we're comparing the new Username with
                return True # If they match, it means they're the same and it's already existing so we return true
            line = namehandle.readline()
        return False


    def add_guest_to_file(self, p1,Start): # Function that adds the guest's info to the guest file
        f = open("437Guest.txt", 'a')  # ---text file to temporarily store info of all guest users---
        ID = str(p1.uniqueID)
        f.write(p1.Name + " " + p1.FamilyName + " " + p1.Car.model + " " + p1.Car.platenumber + " " + ID + " "+str(Start))
        f.write("\n")


    def remove_guest_from_file(self, p1): # Removes the corresponding guest's info from the file
        with open("437Guest.txt", "r+") as f:
            d = f.readlines() # Store all the info in the file in a single array
            f.seek(0) # Set the file's current position to the beginning of the file
            ID = str(p1.uniqueID)
            for i in d:
                line = i.split()
                if line[4] != ID:
                    f.write(i) # The corresponding guest (p1)'s info will not be re-written because we're skipping his info 
            f.truncate() # Delete all the info that we had before


    def add_start_time(self,p1,Start): # Given the start time, adds it to the user's information in the user file
        file=""
        Compare=0
        comparisontool=0
        Startlocation=0
        if type(p1)==RegisteredUser:
            file="437User.txt"
            Compare=str(p1.Car.platenumber) # What we will use to compare the information if it's a user
            comparisontool=3 # 3 is the location of the platenumber in each line in the file
            Startlocation=8 # 8 is the location of the Park time in each line in the file
        elif type(p1)==Guest:
            file="437Guest.txt"
            Compare=str(p1.uniqueID) # What we will use to compare the information if it's a guest
            comparisontool=4 # 4 is the location of the ID in each line in the file
            Startlocation=5 # 5 is the location of the Park time in each line in the file
        with open(file, "r+") as f:
            file = f.readlines()
            f.seek(0)
            for row in file:
                line = row.split()
                # print(line)
                if line[comparisontool] != Compare: # For users, we use their car's platenumber to compare
                    f.write(row)
                elif line[comparisontool] == Compare: # When we reach the corresponding user, we re-write his information but with the start time
                    p1.Start=Start
                    line[Startlocation] = str(Start)
                    z = ''
                    for i in range(0, len(line)):
                        z = z + line[i]
                        if i != len(line) - 1:
                            z = z + ' '
                    f.write(z)
                    f.write("\n")
            f.truncate()


    def increment_nb_visits(self, p1): # Increments the number of visits of a certain user in the user file
        with open("437User.txt", "r+") as f:
            file = f.readlines()
            f.seek(0)
            pn = p1.Car.platenumber
            for row in file:
                line = row.split()
                # print(line)
                if line[3] != pn:
                    f.write(row)
                elif line[3] == pn:
                    a = int(line[7]) # Since the numberofvisits is a string in the file, we turn it to an integer, increment it, then we turn it back to a string
                    a += 1
                    line[7] = str(a)
                    z = ''
                    for i in range(0, len(line)):
                        z = z + line[i]
                        if i != len(line) - 1:
                            z = z + ' '
                    # print(z)
                    f.write(z)
                    f.write("\n")
            f.truncate()
            a=p1.NumberOfVisits
            a=int(a)
            a+=1
            p1.NumberOfVisits=str(a)


    def add_user_to_file(self, p1): # When a new user registers, we add his information to the file
        namehandle = open("437User.txt", 'a')
        namehandle.write(
            p1.Name + " " + p1.FamilyName + " " + p1.Car.model + " " + p1.Car.platenumber + " " + p1.Username + " " + p1.Password + " " + p1.BankAccountNumber + " 0"+" 0")
        namehandle.write("\n")


    def user_options(self, p1): # Displays the options available for users: park - check location - release car - exit
        while True:
            print("Choose one of the following options and type it below: ")
            print("If you want to park your car, enter 'park'")
            print("If your car is already parked and you want to check your car location enter 'location'")
            print("If your car is already parked and you want to release it enter 'release'")
            print("If you want to sign out enter 'exit'")
            enter = input()
            if enter == 'park':
                state = p1.park_car()
                if (state == -1):  # PARKING IS FULL
                    print("Parking is Full. Please Check Other Parkings.\n")
                    return
            elif enter == 'location':
                p1.check_car_location()
            elif enter == 'exit':
                del p1  # WHEN THE USER WANTS TO EXIT, WE JUST DELETE P1 (USER)
                print("You successfully exitted")
                break
            elif enter == 'release':
                (boolean,irrelevant)=self.CarRotationManager.check_if_user_parked(p1)
                if boolean==False:
                    print("Your car is not parked")
                else:
                    if int(p1.NumberOfVisits)%10==0: #for every multiple of 10 visit (10 visits, 20 visits,...), the user gets a free parking for the day
                        print("Today is your " + str(p1.NumberOfVisits) + "th visit!")
                        print("Your bill today is free of charge! Thank you for visiting us " + p1.Name)
                        service_time = self.CarRotationManager.get_delay(p1) # Gets the delay required for the car to be released
                        print("Your car is being released, please wait. Time estimated: " + str(
                            service_time) + " seconds.")
                        time.sleep(service_time) # Wait out till the delay has passed and then release the car
                        print("Your " + p1.Car.model + " is always in safe hands.")
                        p1.request_car()
                        return
                    else:
                        print("To release your car, you should pay first.")
                        payment=self.get_payment(p1) # Get the payment due on the user (which depends on how much time the user has kept his car in the parking)
                        print("Total Bill: " +str(payment) + " L.L")
                        print("To pay by cash, enter 'cash'")
                        print("To pay by credit card, enter 'credit'")
                        Input = input("")
                        while True:
                            if Input.lower() == 'cash':
                                print("You can now pay to the machine administator.")
                                service_time = self.CarRotationManager.get_delay(p1) # Gets the delay required for the car to be released
                                print("Your car is being released, please wait. Time estimated: " + str(
                                    service_time) + " seconds.")
                                time.sleep(service_time) # Wait for the delay to be finished
                                p1.request_car()
                                return
                            elif Input.lower() == 'credit':
                                print("Payment is successful.")
                                service_time = self.CarRotationManager.get_delay(p1) # Gets the delay required for the car to be released
                                print("Your car is being released, please wait. Time estimated: " + str(
                                    service_time) + " seconds.")
                                time.sleep(service_time) # Wait for the delay to be finished
                                p1.request_car()
                                return
                            else:
                                print("Invalid input.")
                                print("To pay by cash, enter 'cash'")
                                print("To pay by credit card, enter 'credit'")
                                Input = input("")
            else:
                print("Invalid input")


    def get_payment(self,p1): # Function that calculates the payment due on the guest based on the time his car stayed in the parking
        Start=''
        comparisontool=0
        retrieve=0
        hourlybill=0
        Compare=0
        if type(p1)==Guest:
            f=open('437Guest.txt')
            comparisontool=4
            retrieve=5
            hourlybill=1500 # We want to charge guests more than registered users, 1,500 LL for 1 hour of parking time
            Compare=p1.uniqueID
        if type(p1)==RegisteredUser:
            f=open('437User.txt')
            comparisontool=3
            retrieve=8
            hourlybill=1000 # For users, it's 1000 LL per hour
            Compare=p1.Car.platenumber
        file = f.readlines()
        for row in file:
            line = row.split()
            if str(line[comparisontool]) == str(Compare):
                Start=str(line[retrieve])
                break
        new_var1 = Start.split("@")
        date1 = [float(x) for x in (new_var1[0]).split("-")] # We're turning the values of the years-months-days from string to float
        time1 = [float(x) for x in (new_var1[1]).split(":")] # We're turning the values of the hours-seconds-minutes from string to float
        now2 = datetime.now() # This corresponds to the time when the guest asks to release his car
        new_var2 = str(now2).split()
        date2 = [float(x) for x in (new_var2[0]).split("-")] # We're turning the values of the years-months-days from string to float
        time2 = [float(x) for x in (new_var2[1]).split(":")] # We're turning the values of the hours-seconds-minutes from string to float
        T2 = ((time2[0]*(60*60) + time2[1]*(60) + time2[2])+ date2[0]*(365*24*60*60) + date2[1]*(30*24*60*60) + date2[2]*(24*60*60))
        T1 = ((time1[0]*(60*60) + time1[1]*(60)  + time1[2])+date1[0]*(365*24*60*60) + date1[1]*(30*24*60*60)  + date1[2]*(24*60*60))
        TimeDiff = abs(T2-T1) # Absolute time difference between parking and releasing, in seconds
        f.close()
        billval=(TimeDiff/3600)*(hourlybill) 
        return math.ceil(billval)


    def guest_options(self, p1): # Function that displays the options available for guests
        while True:
            print("Choose one of the following options and type it below: ")
            print("If you want to park your car, enter 'park'")
            print("If your car is already parked and you want to release it enter 'release'")
            print("If you want to sign out enter 'exit'")
            enter = input()
            if enter == 'park':
                state = p1.park_car()
                if (state == -1):  # PARKING IS FULL
                    print("Parking is Full. Please Check Other Parkings.\n")
                    return
            elif enter == 'exit':
                del p1  # WHEN THE USER WANTS TO EXIT, WE FIRST REMOVE THE GUEST FROM THE FILE, THEN WE DELETE P1 (GUEST)
                print("You successfully exitted\n")
                break
            elif enter == 'release':
                (boolean,irrelevant)=self.CarRotationManager.check_if_guest_parked(p1)
                if boolean==False:
                    print("Your car is not parked!")
                else:
                    print("To release your car, you should pay first.")
                    payment=self.get_payment(p1)
                    print("Total Bill: "+str(payment) + " L.L")
                    print("To pay by cash, enter 'cash'")
                    print("To pay by credit card, enter 'credit'")
                    Input = input("")
                    while True:
                        if Input.lower() == 'cash':
                            print("You can now pay to the machine administator.")
                            service_time = self.CarRotationManager.get_delay(p1)
                            print("Your car is being released, please wait. Time estimated: " + str(
                                service_time) + " seconds.")
                            time.sleep(service_time)
                            p1.request_car()
                            return
                        elif Input.lower() == 'credit':
                            ccn = int(input("Enter your credit card number:"))
                            while (type(ccn) != int):
                                print("Invalid Input.")
                                ccn = int(input("Enter your credit card number:"))
                            print("Payment is successful.")
                            service_time = self.CarRotationManager.get_delay(p1)
                            print("Your car is being released, please wait. Time estimated: " + str(
                                service_time) + " seconds.")
                            time.sleep(service_time)
                            p1.request_car()
                            return
                        else:
                            print("Invalid input.")
                            print("To pay by cash, enter 'cash'")
                            print("To pay by credit card, enter 'credit'")
                            Input = input("")
            else:
                print("Invalid input\n")