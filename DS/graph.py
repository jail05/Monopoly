class Graph:
    def __init__(self):
        # adjacency list وزندار
        self.adj_list = {}

    def add_edge(self, payer_id, receiver_id, amount):
        if payer_id not in self.adj_list:
            self.adj_list[payer_id] = {}

        if receiver_id not in self.adj_list[payer_id]:
            self.adj_list[payer_id][receiver_id] = 0

        self.adj_list[payer_id][receiver_id] += amount
