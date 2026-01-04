class Client:
    def __init__(self, game_state, server):
        self.game_state = game_state
        self.server = server


    def roll_dice(self):
        dice = self.server.roll_dice()
        self.game_state.move_current_player(dice)

    def buy_property(self):
        self.game_state.buy_current_property()

    def end_turn(self):
        self.game_state.end_turn()

    def get_chance_card(self):
        self.game_state.get_chance_card()


    def show_ststus(self):
        player = self.game_state.current_player
        print("Player: ", player.name)
        print("Balance: ", player.balance)
        print("Position: ", player.current_tile.tile_id)

