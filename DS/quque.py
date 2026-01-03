class Queue:
    def __init__(self):
        self.items = []

    def enqueue(self , amount):
        self.items.append(amount)

    def dequeue(self):
        if len(self.items) == 0 :
            print("is Empty!")
            return
        return self.items.pop(0)

    def makeNull(self):
        self.items = []

