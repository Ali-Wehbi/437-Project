from CircularDoublyLinkedList import CircularDoublyLinkedList
from Platform import Platform

class CarRotationManager:
    def __init__(self, Name, NumPlatforms):
        self.Name = Name
        self.NumPlatforms = NumPlatforms
        self.basepos = NumPlatforms // 2
        self.llist = CircularDoublyLinkedList()
        for i in range(0, NumPlatforms):
            platform = Platform(i, Name + str(i))  # ex: For Parking A , we have platforms of names: A1,A2,A3....
            self.llist.append(platform)
        self.set_base() 
        self.occupiedPlatforms = 0 # Initially, no cars are parked
        """self.llist = llist"""

    def isFull(self): # Checks if the parking is full
        if (self.occupiedPlatforms != self.NumPlatforms):  # Parking is not full
            return False
        return True

    def parking_info(self): # Prints whether the parking is full or not, and if not then also prints how many empty spots are there
        print("Parking " + self.Name + " Info:")
        if (self.isFull() == True):
            print("Parking " + self.Name + " is Full. Please check the other parkings.")
        else:
            print(
                "There are " + str(self.NumPlatforms - self.occupiedPlatforms) + " empty spots in Parking " + self.Name)
            print("You can proceed to this parking.\n")

    def check_if_guest_parked(self, guest): # Function which takes the guest as input, and checks if his/her car is parked
        x = guest.uniqueID
        i = 0
        node = self.llist.head
        while i < self.llist.length:
            z = node.data.linkedperson
            if z != "NULL" and type(guest) == type(z): # If we find an ID which matches the guest's ID in the parking, it means the car is parked
                if int(z.uniqueID) == int(x): # Comparison being made with respect to guest ID
                    return (True, node.data) # Return the platform on which the guest is parked
            node = node.next
            i += 1
        return (False, None)

    def check_if_user_parked(self, user):
        i = 0
        node = self.llist.head
        while i < self.llist.length:
            if node.data.linkedperson != "NULL": # If we find a plate number which matches the plate number of the user's car in the parking, it means it's parked
                if node.data.linkedperson.Car.platenumber == user.Car.platenumber: # Comparison being made with respect to plate number of the car
                    return (True, node.data) # Return the platform on which the user is parked
            node = node.next
            i += 1
        return (False, None)

    def set_base(self): # Sets the base position in the middle, i.e if we have 12 platforms, the base position is 6
        basepos = self.llist.length // 2 # Base position will be in the middle, so base pos = (length of list / 2)
        point = self.llist.head
        while point.data.Position != basepos: # We compare each node's position with the base pos, once we find it we exit the loop
            point = point.next
        self.llist.base = point

    def get_platform_position(self, User): # Given a user, we search for the platform where the car is parked
        tempnode = self.llist.head
        i = 0
        x = User.Car.platenumber
        while i < self.llist.length:
            if (tempnode.data.linkedperson != "NULL"):
                if (tempnode.data.linkedperson.Car.platenumber == x): # Comapring users' cars with respect to unique plate numbers.
                    return tempnode.data.Position
            tempnode = tempnode.next
            i += 1
        print("Your Car is not parked in this parking.")
        return -1 # If his car is not parked, then we return -1 as the position

    def get_platform_level(self, User): # Function that checks on which level the user's car is parked
        pos = self.get_platform_position(User) #Car is not parked
        if pos == -1:
            return -1
        else:
            level = abs(pos - self.basepos) # calculates the level with respect to the base position
        return level

    def get_delay(self,User): #Calculates the time taken to move the car of a user from its level to the base position.
        level = self.get_platform_level(User)
        if level==0:
            delay = 0 #Platform is already on ground level, no rotation delay
        else:
            delay = 10 #Rotation delay in seconds, provided by us
        return level*delay #Time taken in seconds for the car to arrive to the base level.

    def get_platform_name(self, User): # In case the user wants to know the location of their car, this function returns the platform on which the car is parked
        tempnode = self.llist.head
        i = 0
        x = User.Car.platenumber
        while i < self.llist.length:
            if (tempnode.data.linkedperson != "NULL"):
                if (tempnode.data.linkedperson.Car.platenumber == x): # Comparison being made with respect to plate numbers
                    return tempnode.data.name
            tempnode = tempnode.next
            i += 1
        print("Your Car is not parked in this parking.")
        return None

    def return_platform_to_base(self, pos):  # moves the platform at position pos to the base position.
        tempnode = self.llist.head
        i = 0
        while i < self.llist.length:
            if (pos == tempnode.data.Position):
                steps = abs(
                    tempnode.data.Position - self.basepos)  # In our Parking structure in the report, we have assigned the basepos to be at position 6
                if tempnode.data.Position <= self.basepos:
                    rotate_clockwise = False # If the car is on the right side of the parking, then we must rotate the ferris wheel clockwise (because it would take less steps to reach base)
                else:
                    rotate_clockwise = True # If the car is on the left side of the parking, then we must rotate the ferris wheel anticlockwise (because it would take less steps to reach base)
                tempnode.data.Position = self.basepos
                break
            tempnode = tempnode.next
            i += 1
        self.update_positions(steps, tempnode.data.name, rotate_clockwise) #updates positions of all platforms according to the number of steps passed

    def update_positions(self, steps, NewBaseName,
                         rotate_clockwise):  # updates the positions of all platforms (Rotating by a specific number of steps passed)
        tempnode = self.llist.head
        i = 0
        if rotate_clockwise == True: # If the rotation is clockwise, then to update the positions we need to subtract from them the number of steps
            while i < self.llist.length:
                if (tempnode.data.name != NewBaseName):
                    if tempnode.data.Position >= steps:
                        tempnode.data.Position = tempnode.data.Position - steps 
                    else: # If the position < number of steps, we apply the same formula, however we need to add the size of the list to get the correct position
                        tempnode.data.Position = tempnode.data.Position - steps + self.llist.length
                tempnode = tempnode.next
                i += 1
        elif rotate_clockwise == False:
            while i < self.llist.length:
                if (tempnode.data.name != NewBaseName):
                    if tempnode.data.Position + steps <= (self.NumPlatforms - 1):
                        tempnode.data.Position = tempnode.data.Position + steps
                    else: # If the position > steps, we apply the same formula, however we need to subtract the size of the list to get the correct position
                        tempnode.data.Position = tempnode.data.Position + steps - self.llist.length
                tempnode = tempnode.next
                i += 1
        return  # END OF FUNCTION

    def release_car(self, Platform):
        # Assuming now that the platform is at the base position
        Platform.linkedperson = "NULL"

    def return_empty_platform(self):
        # FUNCTION THAT FINDS AND RETURNS THE CLOSEST EMPTY PLATFORM TO THE BASE POSITION
        i = 0
        tempnode = self.llist.head
        mindistance = self.llist.length
        minnode = None
        while i < self.llist.length: # This loop finds the closest empty platform to the base position
            steps = abs(tempnode.data.Position - self.basepos)
            if steps < mindistance and tempnode.data.linkedperson == "NULL": # Loop over ever empty platform, and check distance to base position and keep updating min distance
                mindistance = steps
                minnode = tempnode
            i += 1
            tempnode = tempnode.next

        if mindistance == self.llist.length: # If we did not find any empty platform, then mindistance will retain it's initial value that we gave it (list length)
            return None
        else:
            return minnode.data