class Heap:
    def __init__(self):
        self.heap = []


    def insert(self, val):
        self.heap.append(val)
        self.heap.sort(reverse=True)

    def get_max(self):
        if self.heap:
            return self.heap[0]
        else:
            return None

    