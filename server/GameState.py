from Monopoly.server.board import Board
from Monopoly.server.player import Player
from ..DS .HashTable import Dynamic_HashTable


class GameState:
    def __init__(self):
        self.players = Dynamic_HashTable(5)
        self.initialize_players()
        self.current_player_index = 1
        self.board = Board()
        self.round_number = 0
        self.roll_dice = None
        self.game_over = False

    def initialize_players(self):
        player1 = Player("A",self.board.get_tiles())
        player2 = Player("B",self.board.get_tiles())
        player3 = Player("C",self.board.get_tiles())
        player4 = Player("D",self.board.get_tiles())
        self.players.insert(1,player1)
        self.players.insert(2,player2)
        self.players.insert(3,player3)
        self.players.insert(4,player4)

    def remove_player(self, player):
       self.current_player_index = (self.current_player_index + 1) % 4
       # self.player.



