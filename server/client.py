class Client:
    def __init__(self, server, name):
        self.server = server
        self.name = name
        self.client_id = id(self)
        self.player_id = None

    def connect(self):
        response = self.server.handle_request(
            self.client_id,
            {"type": "HELLO", "name": self.name}
        )
        self.player_id = response["player_id"]
        print("Connected as Player", self.player_id)

    def roll_dice(self):
        return self.server.handle_request(self.client_id, {"type": "ROLL_DICE"})


    def end_turn(self):
        return self.server.handle_request(self.client_id, {"type": "END_TURN"})


    def undo(self):
        return self.server.handle_request(self.client_id, {"type": "UNDO"})

    def redo(self):
        return self.server.handle_request(self.client_id, {"type": "REDO"})

