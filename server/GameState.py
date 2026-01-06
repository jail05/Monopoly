import heapq

from Monopoly.server.board import Board
from Monopoly.server.player import Player
from ..DS .HashTable import Dynamic_HashTable
from .property import Property
from ..DS.Heap import Heap
from ..DS.BinaryTree import Tree
from ..DS.graph import Graph


class GameState:
    def __init__(self):
        self.players = Dynamic_HashTable(5)
        self.properties = Dynamic_HashTable(20)
        self.board = Board()
        self.initialize_players()
        self.initialize_properties()
        # self.current_player_index = current_player
        self.round_number = 0
        # self.roll_dice = None
        self.game_over = False
        self.financial_graph = Graph()


    def initialize_players(self):
        player1 = Player("A",self.board.get_tiles())
        player2 = Player("B",self.board.get_tiles())
        player3 = Player("C",self.board.get_tiles())
        player4 = Player("D",self.board.get_tiles())
        self.players.insert(1,player1)
        self.players.insert(2,player2)
        self.players.insert(3,player3)
        self.players.insert(4,player4)

    def add_player(self, player: Player):
        self.players.insert(player.id, player)

    def initialize_properties(self):
        COLOR_GROUPS = {
            "BROWN": 2,
            "LIGHT_BLUE": 3,
            "PINK": 3,
            "ORANGE": 3,
            "RED": 3,
            "YELLOW": 3,
            "GREEN": 3,
        }
        for color, count in COLOR_GROUPS.items():
            for i in range(count):
                name = f"{color}_{i + 1}"
                p = Property(name=name,color=color)
                self.properties.insert(p.ID,p)

    def remove_player(self, player):
       # self.current_player_index = (self.current_player_index + 1) % 4
       player.own_properties.clear_all_properties()
       player.bankrupt()

    def snapshot(self):
        players_snapshot = {}

        for item in self.players.table:
            if item is not None:
                pid, player = item
                players_snapshot[pid] = {
                    "balance": player.balance,
                    "tile": player.current_tile.id,
                    "state": player.state
                }

        return {
            "players": players_snapshot,
            "current_player": self.current_player_index,
            "round": self.round_number,
            "game_over": self.game_over
        }


    def report_top_k_balance(self, k=3):
        heap = Heap()

        for item in self.players.table:
            if item is not None:
                pid, player = item
                heap.insert((player.balance, player.name))

        result = []
        for i in range(k):
            top = heap.get_max()
            if top is None:
                break
            result.append(top)
            heap.heap.remove(top)

        return result

    def report_top_k_properties(self, k=3):
        heap = Heap()

        for item in self.players.table:
            if item is not None:
                pid, player = item
                count = player.own_properties.get_property_count()
                heap.insert((count, player.name))

        result = []
        for i in range(k):
            top = heap.get_max()
            if top is None:
                break
            result.append(top)
            heap.heap.remove(top)

        return result

    def report_top_k_rent(self, k=3):
        heap = Heap()

        for item in self.players.table:
            if item is not None:
                pid, player = item
                heap.insert((player.total_rent_value(), player.name))

        result = []
        for _ in range(k):
            top = heap.get_max()
            if top is None:
                break
            result.append(top)
            heap.heap.remove(top)

        return result

    def pay_rent(self, payer: Player, owner: Player, amount: int):
        success = payer.pay(amount)
        if success:
            owner.recieve(amount)

            self.financial_graph.add_edge(payer.id, owner.id, amount)

    def report_sorted_players_by_balance(self):
        bst = Tree()

        for item in self.players.table:
            if item is not None:
                pid, player = item
                bst.insert(player.balance, player.name)

        return bst.print_inorder()


    def report_top_k_payers(self, k=3):
        heap = Heap()
        for u in self.financial_graph.adj_list:
            total = sum(self.financial_graph.adj_list[u].values())
            heap.insert((total, u))
        return heap.extract_top_k(k)

    def report_top_k_receivers(self, k=3):
        incoming = {}
        for u in self.financial_graph.adj_list:
            for v, w in self.financial_graph.adj_list[u].items():
                incoming[v] = incoming.get(v, 0) + w

        heap = Heap()
        for pid, total in incoming.items():
            heap.insert((total, pid))
        return heap.extract_top_k(k)

    def report_top_k_interactions(self, k=3):
        heap = Heap()
        for u in self.financial_graph.adj_list:
            for v, w in self.financial_graph.adj_list[u].items():
                heap.insert((w, (u, v)))
        return heap.extract_top_k(k)
