from random import randint
from enum import Enum, auto
from GameState import GameState
from Monopoly.server.player import Player
from Monopoly.server.property import Property


class RequestType(Enum):
    HELLO = auto()
    ROLL_DICE = auto()
    BUY_PROPERTY = auto()
    END_TURN = auto()
    UNDO = auto()
    REDO = auto()


class Server:
    def __init__(self):
        self.game_state = GameState()
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


    def handle_trade(self, player_id, trade_data):
        player = self.game_state.players.search(player_id)[1]
        other = self.game_state.players.search(trade_data["to"])[1]

        success = player.propose_trade(
            other,
            trade_data["give_money"],
            trade_data["give_properties"],
            trade_data["take_money"],
            trade_data["take_properties"]
        )

        if success:
            self.game_state.financial_graph.add_edge(player.id, other.id)

        return success

    def handle_landing_on_property(self, player: Player, property: Property):
        if property.has_owner() and property.owner_id != player.id:
            owner = self.players.search(property.owner_id)[1]
            rent = property.current_rent()
            self.pay_rent(player, owner, rent)

