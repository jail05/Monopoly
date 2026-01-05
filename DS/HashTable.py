class Dynamic_HashTable:
    def __init__(self, max_size):
        self.max_size = max_size
        self.table = [None] * self.max_size
        self.size = 0

    def hash(self, key):
        if not isinstance(key, int):
            key = hash(key)
        return key % self.max_size

    def insert(self, key, value):
        if self.size == self.max_size:
            self.resize()
        k = self.hash(key)
        while self.table[k] is not None:
            k = (k + 1) % self.max_size
        self.table[k] = (key, value)
        self.size += 1

    def resize(self):
        old = self.table
        self.max_size *= 2
        self.table = [None] * self.max_size
        self.size = 0

        for item in old:
            if item is not None:
                self.insert(item[0], item[1])

    def search(self, key):
        k = self.hash(key)
        k2 = self.hash(key)

        while self.table[k] is not None:
            if self.table[k][0] == key:
                return self.table[k]
            k = (k + 1) % self.max_size
            if k == k2:
                break
        return -1

    def delete(self, key):
        k = self.hash(key)
        k2 = self.hash(key)

        while self.table[k] is not None:
            if self.table[k][0] == key:
                m = self.table[k]
                self.table[k] = None
                self.size -= 1
                return m
            k = (k + 1) % self.max_size
            if k == k2:
                break
        return -1

    def display(self):
        for i in range(self.max_size):
            if (self.table[i] is not None):
                print("key =", self.table[i][0], "  value=", self.table[i][1])



