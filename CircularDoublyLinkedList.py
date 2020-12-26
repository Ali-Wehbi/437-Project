from Node import Node

class CircularDoublyLinkedList:
    # Constructor for empty Doubly Linked List
    def __init__(self):
        self.head = None
        self.tail = None
        self.base = None
        self.length = 0

    def append(self, new_data): #appends nodes at the end of the linked list.
        new_node = Node(new_data)
        new_node.next = None
        self.length = self.length + 1
        if (self.head is None):
            new_node.prev = None
            self.head = new_node
            self.tail = new_node
            return
        self.tail.next = new_node
        new_node.prev = self.tail   #updating node.prev to the tail(which is at the end of the list).
        new_node.next = self.head   #updating node.next to the head(to make it circular)
        self.head.prev = new_node
        self.tail = new_node  #update the tail to be the new node.
        return

    def print_list(self, node): #Passes through all nodes(platforms) of the list and prints the data associated with each node.
        #(Data includes: the name of the platform, its position, and which car is on it, if any)
        i = 0
        while (i < self.length):
            print(node.data)
            # last = node
            node = node.next
            i = i + 1