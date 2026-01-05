from random import randint
from enum import Enum, auto
from GameState import GameState


class RequestType(Enum):
    HELLO = auto()
    ROLL_DICE = auto()
    BUY_PROPERTY = auto()
    END_TURN = auto()
    UNDO = auto()
    REDO = auto()
from ..DS .graph import Graph

class Server:
    def __init__(self):
        self.current_player = 1
        self.game_state = GameState(self.current_player)
        self.financial_graph = Graph()
        self.clients = {}
        self.current_turn = 0
        self.game_over = False



    def handle_hello(self, client_id, player_name):
        if len(self.game_state.players) >= 4:
            return {"type": "ERROR", "message": "Game is full"}

        player = self.game_state.add_player(player_name)
        self.clients[client_id] = player.id

        return {
            "type": "WELCOME",
            "player_id": player.id,
            "balance": player.balance
        }

    def handle_roll_dice(self, client_id):
        if self.game_over:
            return {"type": "ERROR", "message": "Game Over"}

        player = self.get_current_player(client_id)
        dice = randint(2, 12)

        player.move(dice)
        self.game_state.resolve_tile(player)

        return self.state_update()


    def handle_end_turn(self, client_id):
        self.current_turn = (self.current_turn + 1) % len(self.game_state.players)
        return self.state_update()


    def handle_undo(self, client_id):
        player = self.get_current_player(client_id)
        player.undo_action()
        return self.state_update()

    def handle_redo(self, client_id):
        player = self.get_current_player(client_id)
        player.redo_action()
        return self.state_update()


    def handle_request(self, client_id, request):
        rtype = request["type"]

        if rtype == RequestType.HELLO:
            return self.handle_hello(client_id, request["name"])

        if rtype == RequestType.ROLL_DICE:
            return self.handle_roll_dice(client_id)

        if rtype == RequestType.END_TURN:
            return self.handle_end_turn(client_id)

        if rtype == RequestType.UNDO:
            return self.handle_undo(client_id)

        if rtype == RequestType.REDO:
            return self.handle_redo(client_id)



    def get_current_player(self, client_id):
        pid = self.clients[client_id]
        return self.game_state.players[pid]



    def state_update(self):
        return {
            "type": "STATE_UPDATE",
            "state": self.game_state.snapshot()
        }


