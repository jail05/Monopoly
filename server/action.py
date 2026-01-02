from enum import Enum, auto

class ActionType(Enum):
    Move = auto()
    BuyProperty = auto()
    PayRent = auto()
    Trade = auto()
    Build = auto()
    Mortgage = auto()
    CardEffect = auto()

class Action:
    ID=0
    def __init__(self, id):
        Action.ID +=1
        self.action_id = Action.ID
        self.action_type = ActionType.Move
        self.actor_id = id
        self.affected_entities= []
        self.previous_state = None
        self.new_state = None

