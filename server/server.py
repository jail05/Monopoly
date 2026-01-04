from random import random
from typing import Hashable


class Server:
    def __init__(self):
        self.players = Hashable()
        self.properties = Hashable()


    def roll_dice(self):
        return random.randint(2,12)




