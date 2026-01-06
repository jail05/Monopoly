from random import randint
from GameState import GameState
from .chanceCard import ChanceCard
from .player import *

class RequestType(Enum):
    HELLO = auto()
    ROLL_DICE = auto()
    BUY_PROPERTY = auto()
    END_TURN = auto()
    UNDO = auto()
    REDO = auto()


class Server:
    def __init__(self):
        # self.current_player = 1
        self.game_state = GameState()
        # self.financial_graph = Graph()
        self.clients = {}
        self.players_id = []
        self.current_turn = 0
        self.chance_card = ChanceCard()
        self.turn_order = []  # ترتیب چرخش بازیکن‌ها
        self.current_player_index = 0  # اندیس بازیکن فعلی
        self.pending_action = None  # برای BUY_PROPERTY

        # self.game_over = False
    #
    # def initialize_players(self):
    #     player1 = Player("A",self.game_stateboard.get_tiles())
    #     player2 = Player("B",self.board.get_tiles())
    #     player3 = Player("C",self.board.get_tiles())
    #     player4 = Player("D",self.board.get_tiles())
    #     self.players.insert(1,player1)
    #     self.players.insert(2,player2)
    #     self.players.insert(3,player3)
    #     self.players.insert(4,player4)
    #
    # def handle_hello(self, client_id, player_name):
    #     if len(self.game_state.players) >= 4:
    #         return {"type": "ERROR", "message": "Game is full"}
    #
    #     player = self.game_state.add_player(player_name)
    #     self.clients[client_id] = player.id
    #
    #     return {
    #         "type": "WELCOME",
    #         "player_id": player.id,
    #         "balance": player.balance
    #     }
    #
    # def handle_roll_dice(self, client_id):
    #     if self.game_over:
    #         return {"type": "ERROR", "message": "Game Over"}
    #
    #     player = self.get_current_player(client_id)
    #     dice = randint(2, 12)
    #
    #     player.move(dice)
    #     self.game_state.resolve_tile(player)
    #
    #     return self.state_update()
    #
    #
    # def handle_end_turn(self, client_id):
    #     self.current_turn = (self.current_turn + 1) % len(self.game_state.players)
    #     return self.state_update()
    #
    #
    # def handle_undo(self, client_id):
    #     player = self.get_current_player(client_id)
    #     player.undo_action()
    #     return self.state_update()
    #
    # def handle_redo(self, client_id):
    #     player = self.get_current_player(client_id)
    #     player.redo_action()
    #     return self.state_update()
    #
    #
    # def handle_request(self, client_id, request):
    #     rtype = request["type"]
    #
    #     if rtype == RequestType.HELLO:
    #         return self.handle_hello(client_id, request["name"])
    #
    #     if rtype == RequestType.ROLL_DICE:
    #         return self.handle_roll_dice(client_id)
    #
    #     if rtype == RequestType.END_TURN:
    #         return self.handle_end_turn(client_id)
    #
    #     if rtype == RequestType.UNDO:
    #         return self.handle_undo(client_id)
    #
    #     if rtype == RequestType.REDO:
    #         return self.handle_redo(client_id)
    #
    #
    #
    # def get_current_player(self, client_id):
    #     pid = self.clients[client_id]
    #     return self.game_state.players[pid]
    #
    #
    #
    # def state_update(self):
    #     return {
    #         "type": "STATE_UPDATE",
    #         "state": self.game_state.snapshot()
    #     }
    #
    #
    def init_players(self):
        for name in ["A", "B", "C", "D"]:
            player = Player(name, self.game_state.board.get_tiles())
            self.game_state.add_player(player)
            self.turn_order.append(player.id)

    def get_current_player(self):
        pid = self.turn_order[self.current_player_index]
        return self.game_state.players.search(pid)[1]

    def is_players_turn(self, client_id):
        return self.clients.get(client_id) == self.get_current_player().id

    def start_turn(self):
        self.pending_action = None

    def roll_dice(self, player):
        dice = randint(2, 12)
        player.move(dice)
        self.process_tile(player)

    def process_tile(self, player):
        tile = player.current_tile.data

        if tile and isinstance(tile, dict) and "price" in tile:
            self.handle_property(player, tile)

        elif tile == "CARD":
            self.handle_chance_card(player)

        elif isinstance(tile, int):
            player.pay(tile)

    def handle_property(self, player, tile_data):
        owner_id = tile_data["owner"]

        if owner_id is None:
            # فقط اطلاع به کلاینت
            self.pending_action = {
                "type": "BUY_OPTION",
                "player_id": player.id,
                "property_id": tile_data["id"]
            }
            return
        else:
            owner = self.game_state.players.search(owner_id)[1]
            rent = tile_data["rent"]
            self.game_state.pay_rent(player, owner, rent)

    def handle_buy_property(self, client_id, property_id):
        if self.pending_action is None:
            return {"type": "ERROR", "message": "No property to buy"}

        if self.pending_action["player_id"] != self.get_current_player().id:
            return {"type": "ERROR", "message": "Not your pending action"}

        if self.pending_action["property_id"] != property_id:
            return {"type": "ERROR", "message": "Invalid property"}

        player = self.get_current_player()
        prop = self.game_state.properties.search(property_id)[1]

        if prop.owner_id is not None:
            return {"type": "ERROR", "message": "Already owned"}

        if not player.pay(prop.purchase_price):
            return {"type": "ERROR", "message": "Not enough money"}

        prop.set_owner_id(player.id)
        player.add_property(prop)

        self.pending_action = None
        return self.state_update()

    def handle_chance_card(self, player):
        card = self.chance_card.getCard()  # dequeue
        player.apply_card_effect(card)

        # اگر کارت قابل نگه‌داری بود (Get out of jail)
        if card.effect_type != CardEffectType.GET_OUT_OF_JAIL:
            self.chance_card.returnCard(card)

    def end_turn(self):
        self.current_player_index = (self.current_player_index + 1) % len(self.turn_order)
        self.game_state.round_number += 1


    def pay_rent(self, payer: Player, owner: Player, amount):
        if payer.pay(amount):
            owner.recieve(amount)
            self.game_state.financial_graph.add_edge(payer.id, owner.id)


    def handle_request(self, client_id, request):
        rtype = request["type"]

        if rtype == "HELLO":
            return self.handle_hello(client_id, request["name"])

        if not self.is_players_turn(client_id):
            return {"type": "ERROR", "message": "Not your turn"}

        if rtype == "UNDO" and self.pending_action is not None:
            return {"type": "ERROR", "message": "Finish current action first"}

        player = self.get_current_player()

        if rtype == "ROLL_DICE":
            self.roll_dice(player)

        elif rtype == "END_TURN":
            self.end_turn()

        elif rtype == "UNDO":
            player.undo_action()

        elif rtype == "REDO":
            player.redo_action()

        elif rtype == "BUY_PROPERTY":
            return self.handle_buy_property(client_id, request["property_id"])

        return self.state_update()

    def handle_hello(self, client_id, name):
        if len(self.turn_order) >= 4:
            return {"type": "ERROR", "message": "Game full"}

        player = Player(name, self.game_state.board.get_tiles())
        self.game_state.add_player(player)

        self.clients[client_id] = player.id
        self.turn_order.append(player.id)

        return {
            "type": "WELCOME",
            "player_id": player.id,
            "balance": player.balance
        }

    def state_update(self):
        return {
            "type": "STATE_UPDATE",
            "state": self.game_state.snapshot()
        }

