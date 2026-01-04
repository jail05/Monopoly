from Monopoly.server.board import Board
from Monopoly.server.player import Player


class GameState:
    def __init__(self):
        self.players = []
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
        self.players.append(player1)
        self.players.append(player2)
        self.players.append(player3)
        self.players.append(player4)

    def remove_player(self, player):
       self.current_player_index = (self.current_player_index + 1) % 4
       # self.player.



