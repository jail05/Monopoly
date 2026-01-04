class Graph:
    def __init__(self):
        self.edges = []

    def add_edge(self, from_player, to_player):
        if from_player not in self.edges:
            self.edges[from_player] = []
            self.edges[from_player].append(to_player)