#Team ArchiTech
# Ali Wehbi - Dania El Tabch - Mohmamad Abdallah - Reine Chami

#-------------------------Guest User---------------------------------------
class Guest:

    def __init__ (self,Name,FamilyName,Car,controlboard,CarRotationManager):     #--Initializing Guest credentials/info---
        self.Name = Name
        self.FamilyName = FamilyName
        self.Car = Car
        self.controlboard = controlboard
        self.CarRotationManager = CarRotationManager
        self.uniqueID = controlboard.SetID()     #----calling controlboard class to set ID---unique ID given by control board/decision engine
    def RequestCar(self): # FUNCTION TO RELEASE CAR
      while True:
        ID = int(input("To release your car, please enter your given ID number: "))
        if ID==self.uniqueID:
            pos=self.CarRotationManager.GetPlatformPosition(self)
            self.CarRotationManager.ReturnPlatformToBase(pos)
            self.CarRotationManager.ReleaseCar(self.linkedplatform)
            print("Your car " + self.Car.model + " is successfully released.")
            break
        else:
            print("Wrong ID entered.")
    def ParkCar(self):
      platform=self.CarRotationManager.ReturnEmptyPlatform() #FOUND CLOSEST EMPTY PLATFORM
      if (platform==None):
          return # PARKING IS FULL
      self.CarRotationManager.ReturnPlatformToBase(platform.Position)
      platform.Link(self) #NOW USER'S CAR IS PARKED ON BASE PLATFORM
      self.linkedplatform=platform


#----------------------------Registered User-----------------------------
class RegisteredUser:
    def __init__(self,Name,FamilyName,Car,Username,Password,BankAccountNumber, controlboard, CarRotationManager,NumberOfVisits=0):   #--Intitializing credentials/info--
        self.Name = Name
        self.FamilyName = FamilyName
        self.Car = Car
        self.Username= Username
        self.Password= Password
        self.BankAccountNumber= BankAccountNumber
        self.NumberOfVisits= NumberOfVisits
        self.controlboard = controlboard
        self.CarRotationManager = CarRotationManager
        self.linkedplatform=None

    def CheckCarLocation(self): #Determines the location of the user's car (Platform name and Platform level that the car sits on)
      name = self.CarRotationManager.GetPlatformName(self)
      level= self.CarRotationManager.GetPlatformLevel(self)
      if level==-1:
        print("Your Car " + self.Car.model + " is not the Parking")
      else:
        print("Your Car " + self.Car.model +  " is on Platform " + name + " and it's on level " + str(level))
  
    def __str__(self): #prints information for a Registered User
      return ("Full name: " + self.Name + " " + self.FamilyName + "\n" +  "Car Model: " + self.Car.model + "\n" +  "Username: " + self.Username + "\n" + "Number of Visits: " + str(self.NumberOfVisits))
    def RequestCar(self): # FUNCTION TO RELEASE CAR
      pos=self.CarRotationManager.GetPlatformPosition(self)
      self.CarRotationManager.ReturnPlatformToBase(pos)
      self.CarRotationManager.ReleaseCar(self.linkedplatform)
    def ParkCar(self):
      platform=self.CarRotationManager.ReturnEmptyPlatform() #FOUND CLOSEST EMPTY PLATFORM
      if (platform==None):
          return # PARKING IS FULL
      self.CarRotationManager.ReturnPlatformToBase(platform.Position)
      platform.Link(self) #NOW USER'S CAR IS PARKED ON BASE PLATFORM
      self.linkedplatform=platform

#------------------------------Car--------------------------------------
class Car:
    def __init__(self,model,platenumber,OwnerName="NULL",OwnerFamilyName="NULL"):  #---Initializing car info---
        self.model=model
        self.platenumber=platenumber
        self.OwnerName= OwnerName
        self.OwnerFamilyName = OwnerFamilyName
    def __str__(self):
        return ("Car Model: " + self.model + "\n" + "Plate Number: " + str(self.platenumber) +  "\n" + "Car Owner: " + self.OwnerName + " " + self.OwnerFamilyName)

#-------------------------Platform--------------------------------------
#Platforms will be distributed on 7 different levels such that the ferris wheel contains 12 parking spaces.
class Platform:
  def __init__(self,Position,name):
    self.Position = Position
    self.name=name
    self.linkedperson = "NULL"
  def __str__(self):   #prints the platform name, and the info of the Car linked to it (if not empty) 
    if self.isEmpty():
      return "Platform " + (self.name) +" is at position "+str(self.Position)+" and it's empty.\n"
    statement = "Platform " + (self.name) + " is at position "+str(self.Position) + ", and on it we have " + self.linkedperson.Name + " " +  self.linkedperson.Car.OwnerFamilyName + "'s " + self.linkedperson.Car.model + "\n"
    return statement
  def Link(self,person):
    self.linkedperson = person
    #print("Platform " + (self.name) + " is linked to Car: " + self.linkedperson.Car.model +  "   Owner: " + self.linkedperson.Car.OwnerName + " " + self.linkedperson.Car.OwnerFamilyName )
  def isEmpty(self):
    if self.linkedperson == "NULL":       #---empty platform---
      #print("Platform is empty")
      return True
    else:                      #---platform nonempty/linked to a person---
      #print("Platform" + (self.name) + " is not empty.\n" + "It is connected to " + self.linkedperson.Name + "'s" + " Car: " + self.linkedperson.Car.model)
      return False


from random import randint
#--------------------------Control Borad------------------------------------
class ControlBoard:
  def __init__(self,CarRotationManager):
    self.IDcounter = 10000
    self.CarRotationManager=CarRotationManager
  def SetID(self):
    self.IDcounter = self.IDcounter + randint(30,90)
    return self.IDcounter
  def Welcome(self):     #---This function allows the user to register/login/continue as a guest---
    Input=input('Would you like to register, login or continue as guest?\n')
    if Input=="register":     #---user wants to create an account / takes info as input from him/her---
        Name=input("Name:\n")
        FamilyName=input("family name:\n")
        model=input("car model:\n")
        platenumber=input("plate number:\n")
        car1=Car(model,platenumber,Name,FamilyName)
        Username=input("username:\n")
        while (self.AlreadyExistingUsername(Username)==True):   #---checks if username is already taken---
            print("Username already exists, please choose a different username:\n")
            Username=input("username:\n")
        Password=input("password:\n")
        BankAccountNumber=input("Bank account number:\n")
        print ("Welcome "+Name+", you have been registered as a user!")
        p1 = RegisteredUser(Name,FamilyName,car1,Username,Password,BankAccountNumber,self,self.CarRotationManager,0)  #---initialize ResgisteredUser---
        self.AddUserToFile(p1)
        return p1
    elif Input=="login":    #---user already has an account and wants to login---
        username=input("Input the username\n")
        password=input("Input the password\n")
        (userbool,passbool,creds)=self.CheckUser(username,password)  #---function to check the username and password---
        while (userbool!=True or passbool!=True):
            if (userbool==True and passbool==False):   #---correct username and wrong password---
                print("Invalid password, Please type the correct password\n")
                password=input("password:\n")
                (userbool,passbool,creds)=self.CheckUser(username,password)
            elif (userbool==False):   #---wrong username---
                print("Incorrect username, please type the correct username and password\n")
                username=input("username:\n")
                password=input("password:\n")
                (userbool,passbool,creds)=self.CheckUser(username,password)
        print("Login sucessful!")
        c1=Car(creds[2],creds[3],creds[0],creds[1])   #---CARNB,PLTNB,NAME,FNAME---
        AlreadyRegisteredUser=RegisteredUser(creds[0],creds[1],c1,creds[4],creds[5],creds[6],self,self.CarRotationManager,creds[7])
        return AlreadyRegisteredUser      
    elif Input=="guest":   #---takes info from the user as input---
        Name=input("Please enter your name:\n")
        FamilyName=input("Please enter your family name:\n")
        model=input("Please enter your car model:\n")
        platenumber=input("Please enter your car's plate number:\n")
        car1=Car(model,platenumber,Name,FamilyName)
        p1=Guest(Name,FamilyName,car1,self,self.CarRotationManager)   #---initialize guest---
        print("Welcome"+" "+Name+"!")
        print("Your ID number is: " + str(p1.uniqueID))
        print("Remember your ID number, you must enter it back to pick up your car.")
        self.AddGuestToFile(p1)
        return p1
    else:
        print("Invalid Input, redirecting you to main page")
        self.Welcome()

  def CheckUser(self,username,password):   #---function to check the username and password---
    namehandle=open("437User.txt")   #---text file that stores all registered users credentials---
    line=namehandle.readline()
    while line!='':
          test=line.split()
          if test[4]==username and test[5]!=password:  #---correct username but wrong password---
              return (True,False,[])
          elif test[4]==username and test[5]==password:  #---correct username and password---
              return (True,True,test)
          line=namehandle.readline()
    return (False,False,[])    #--incorrect user--

  def AlreadyExistingUsername(self,Username):
    namehandle=open("437User.txt")
    line=namehandle.readline()
    while line!='':
        test=line.split()
        if Username==test[4]:
             return True
        line=namehandle.readline()
    return False

  def AddGuestToFile(self,p1):
    f = open("437Guest.txt",'a')    #---text file to temporarily store info of all guest users---
    ID=str(p1.uniqueID)
    f.write(p1.Name+" "+p1.FamilyName+" "+p1.Car.model+" "+p1.Car.platenumber+" "+ID)
    f.write("\n")

  def AddUserToFile(self,p1):
    namehandle=open("437User.txt",'a')
    namehandle.write(p1.Name+" "+p1.FamilyName+" "+p1.Car.model+" "+p1.Car.platenumber+" "+p1.Username+" "+p1.Password+" "+p1.BankAccountNumber+" 0")
    namehandle.write("\n")

#--------------------------Circular Doubly Linked List------------------------------------
class Node: 
  
    # Constructor to create a new node 
    def __init__(self, data): 
        self.data = data 
        self.next = None
        self.prev = None
# Class to create a Doubly Linked List 
class CircularDoublyLinkedList: 
    # Constructor for empty Doubly Linked List 
    def __init__(self): 
        self.head = None
        self.base = None
        self.length = 0

    def append(self, new_data): 
        new_node = Node(new_data) 
        new_node.next = None
        self.length = self.length + 1
        if self.head is None: 
            new_node.prev = None
            self.head = new_node
            return 
        last = self.head 
        while(last.next is not None): 
            last = last.next
        last.next = new_node 
        new_node.prev = last 
        return

    def printList(self, node): 
        i = 0
        while(i<self.length): 
            print(node.data)
            #last = node 
            node = node.next
            i = i+1

    def appendlast(self,new_data): 
        new_node = Node(new_data) 
        new_node.next = None
        self.length = self.length + 1
        if self.head is None: 
            new_node.prev = None
            self.head = new_node 
            return  
        last = self.head 
        while(last.next is not None): 
            last = last.next
        last.next = new_node 
        new_node.prev = last 
        new_node.next = self.head
        return
#--------------------------Car Rotation Manager (Parking) ------------------------------------
#To understand more the structure of our parking, please refer to our report(Refinement Report, page 10) submitted on teams.
class CarRotationManager:
  def __init__(self,llist):
    self.llist = llist
    #self.setBase()
  def setBase(self):
    basepos=self.llist.length//2
    point= self.llist.head
    while point.data.Position!=basepos:
      point=point.next
    self.llist.base=point
    #print("Base: ")
    #print(point.data)
  def GetPlatformPosition(self,User):
    tempnode=self.llist.head
    i=0
    x= User.Car.platenumber
    while i<self.llist.length:
      if (tempnode.data.linkedperson!="NULL"):
          if (tempnode.data.linkedperson.Car.platenumber==x):
              return tempnode.data.Position
      tempnode=tempnode.next
      i+=1
    print("Your Car is not parked in this parking.")
    return -1

  def GetPlatformLevel(self,User):
    pos = self.GetPlatformPosition(User)
    if pos == -1:
      return -1 #Car is not in the parking
    elif pos==6:
      return 0
    elif pos==5 or pos==7:
      return 1
    elif pos==4 or pos==8:
      return 2
    elif pos==3 or pos==9:
      return 3
    elif pos==2 or pos==10:
      return 4
    elif pos==1 or pos==11:
      return 5
    else:
      return 6
    
  def GetPlatformName(self,User):
    tempnode=self.llist.head
    i=0
    x= User.Car.platenumber
    while i<self.llist.length:
      if (tempnode.data.linkedperson!="NULL"):
          if (tempnode.data.linkedperson.Car.platenumber==x):
              return tempnode.data.name
      tempnode=tempnode.next
      i+=1
    print("Your Car is not parked in this parking.")
    return None


  def ReturnPlatformToBase(self,pos): #moves the platform os passed pos to Base.
    tempnode = self.llist.head
    i = 0
    while i<self.llist.length:
      if (pos == tempnode.data.Position):
        steps = abs(tempnode.data.Position - 6) #In our Parking structure, we have assigned the base to be at position 6
        if tempnode.data.Position<=6: 
            RotateClockwise=False
        else:
            RotateClockwise=True
        tempnode.data.Position = 6
        break
      tempnode=tempnode.next
      i += 1
    self.UpdatePositions(steps,tempnode.data.name,RotateClockwise)
    #return steps

  def UpdatePositions(self,steps,NewBaseName,RotateClockwise): #updates the positions of all platforms (Rotating by a specific number of steps passed
    tempnode=self.llist.head
    i=0
    if RotateClockwise==True:
        while i<self.llist.length:
            if (tempnode.data.name!=NewBaseName):
                if tempnode.data.Position>=steps:
                    tempnode.data.Position=tempnode.data.Position-steps
                else:
                    tempnode.data.Position=tempnode.data.Position-steps+self.llist.length
            tempnode=tempnode.next
            i+=1
    elif RotateClockwise==False:
        while i<self.llist.length:
            if (tempnode.data.name!=NewBaseName):
                if tempnode.data.Position+steps<=11:
                    tempnode.data.Position=tempnode.data.Position+steps
                else:
                    tempnode.data.Position=tempnode.data.Position+steps-self.llist.length
            tempnode=tempnode.next
            i+=1
    return # END OF FUNCTION

  def ReleaseCar(self,Platform):
    # Assuming now that the platform is at the base position
    Platform.linkedperson="NULL"

  def ReturnEmptyPlatform(self):
    #FUNCTION THAT FINDS AND RETURNS THE CLOSEST EMPTY PLATFORM TO THE BASE POSITION
    i=0
    tempnode=self.llist.head
    mindistance=self.llist.length
    minnode=None
    while i<self.llist.length:
        steps=abs(tempnode.data.Position-6)
        if steps<mindistance and tempnode.data.linkedperson=="NULL":
            mindistance=steps
            minnode=tempnode
        i+=1
        tempnode=tempnode.next
    
    if mindistance==self.llist.length: 
        print("Parking is full")
        return None
    else:
        return minnode.data


#MAIN CODE
#Creating the linked list
llist = CircularDoublyLinkedList()
#Initializing the positions of each platform to a specific position, and a unique name(A,B,C,...)
platform1 = Platform(0,"A")
platform2 = Platform(1,"B")
platform3 = Platform(2,"C")
platform4 = Platform(3,"D")
platform5 = Platform(4,"E")
platform6 = Platform(5,"F")
platform7 = Platform(6,"G")
platform8 = Platform(7,"H")
platform9 = Platform(8,"I")
platform10 = Platform(9,"J")
platform11 = Platform(10,"K")
platform12 = Platform(11,"L")
#Appending the platforms to the linked list
llist.append(platform1) 
llist.append(platform2) 
llist.append(platform3) 
llist.append(platform4) 
llist.append(platform5)
llist.append(platform6)
llist.append(platform7)
llist.append(platform8)
llist.append(platform9)
llist.append(platform10)
llist.append(platform11)
llist.appendlast(platform12)
#Creating a Parking, with the 12 platforms
Parking=CarRotationManager(llist)
Parking.setBase()
#Creating a control board for the parking
controlboard = ControlBoard(Parking)

#Just for Testing purposes.
#c1 = Car("Lamborghini_Aventador",102929,"Reine","Chami")
#d1 = RegisteredUser("Reine","Chami",c1, "rko123", "password1",192820,controlboard,Parking)
#c2 = Car("Bugatti_Chiron",33884,"Ali","Wehbi")
#d2 = RegisteredUser("Ali","Wehbi",c2, "anw03", "password2", 195824, controlboard,Parking)
#c3 = Car("McLaren_F1",103948,"Dania","Tabch")
#d3 = Guest("Dania","Tabch",c3,controlboard,Parking)
#c4 = Car("Toyota_Corolla",106529,"Mohammad","Abdallah")
#d4 = Guest("Mohammad","Abdallah",c4,controlboard,Parking)

#Just for Testing purposes.
"""
p1 = controlboard.Welcome()
p1.ParkCar()
llist.printList(llist.head)
p1.RequestCar()
p2 = controlboard.Welcome()
p2.ParkCar()
llist.printList(llist.head)
p2.RequestCar()
p2 = controlboard.Welcome()
p2.ParkCar()
llist.printList(llist.head)
p3 = controlboard.Welcome()
p3.ParkCar()
p3.CheckCarLocation()
llist.printList(llist.head)
p4 = controlboard.Welcome()
p4.ParkCar()
llist.printList(llist.head)
p2.RequestCar()
llist.printList(llist.head)
p4.RequestCar()
llist.printList(llist.head)
p3.CheckCarLocation()"""





















