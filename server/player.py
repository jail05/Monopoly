from ..DS.Tree import Tree
from enum import Enum, auto
from ..DS.stack import Stack

class PlayerState(Enum):
    ACTIVE = auto()
    IN_JAIL = auto()
    BANKRUPT = auto()

class Player:
    count = 0
    def __init__(self, name, tile_list):
        self.name = name
        Player.count = Player.count + 1
        self.id = Player.count
        self.balance = 100
        self.current_tile = tile_list.head
        self.own_properties = Tree()
        self.state = PlayerState.ACTIVE
        self.jail_turns = 0
        self.action_history = Stack()



