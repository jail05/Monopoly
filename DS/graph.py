class Graph:
    def __init__(self):
        self.graph = {}

    def add_edge(self, payer_id, receiver_id, amount):
        if payer_id not in self.graph:
            self.graph[payer_id] = {}

        if receiver_id not in self.graph[payer_id]:
            self.graph[payer_id][receiver_id] = 0

        self.graph[payer_id][receiver_id] += amount

    def total_outgoing(self, player_id):
        if player_id not in self.graph:
            return 0
        return sum(self.graph[player_id].values())

    def total_incoming(self, player_id):
        total = 0
        for payer in self.graph:
            total += self.graph[payer].get(player_id, 0)
        return total

    def interactions(self):
        result = []
        for payer in self.graph:
            for receiver, amount in self.graph[payer].items():
                result.append((payer, receiver, amount))
        return result
