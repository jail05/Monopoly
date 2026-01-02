class Stack:
    def __init__(self, capacity):
        self.array = []
        self.capacity = capacity

    def push(self , amount):
        if self.is_full() :
            print("is full!")
            return
        self.array.append(amount)

    def pop(self):
        if len(self.array) == 0:
            print("is Empty!")
            return
        return self.array.pop(len(self.array)-1)

    def peek(self):
        for i in range(len(self.array)):
            print(self.array[i])

    def empty(self):
        self.array = []

    def isEmpty(self):
        if len(self.array) == 0:
            return True
        return False

    def is_full(self):
        if len(self.array) == self.capacity:
            return True
        return False

    def size(self):
        return len(self.array)

    def reverse(self):
        reverse = Stack(self.capacity)
        for i in range(len(self.array)):
            reverse.push(self.pop())
        self.array= reverse.array

    def reverse_recursively(self):
        if len(self.array) == 0:
            return
        top = self.pop()
        self.reverse_recursively()
        self.insert(top)

    def insert(self, top):
        if len(self.array) == 0:
            self.push(top)
            return
        else:
            new_top = self.pop()
            self.insert(top)
            self.push(new_top)







# m = Stack(10)
# m.push(5)
# m.push(2)
# m.push(8)
# m.push(9)
# m.peek()
# m.reverse_recursively()
# m.peek()





