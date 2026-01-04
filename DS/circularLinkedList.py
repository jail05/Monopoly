class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class CircularLinkedList:
    def __init__(self):
        self.head = None

    def Add(self, data):
        new_node = Node(data)
        node = self.head
        if self.head is None:
            self.head = new_node
            new_node.next = new_node
            return
        while node.next != self.head:
            node = node.next
        node.next = new_node
        new_node.next = self.head

    def delete(self,index):
        current = self.head
        if self.head is None:
            print("Empty!")
            return
        if index == 0 and self.head.next==self.head:
            self.head = None
            return

        for i in range(index):
            prev = current
            current = current.next
            if current == self.head:
                print("Index out of range!")
                return
        if current == self.head:
            last = self.head
            while last.next != self.head:
                last = last.next
            self.head = self.head.next
            last.next = self.head
        else:
            prev.next = current.next

    def printNode(self):
        if self.head is None:
            print("Empty!")
            return

        current = self.head
        print(current.data)
        current = current.next

        while current != self.head:
            print(current.data)
            current = current.next


g=CircularLinkedList()
g.Add(1)
g.Add(2)
g.Add(3)
g.printNode()
g.delete(1)
g.printNode()