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
    def __init__(self, action_type, actor_id, affected_entities, previous_state, new_state):
        Action.ID +=1
        self.action_id = Action.ID
        self.action_type = action_type
        self.actor_id = actor_id
        self.affected_entities= affected_entities
        self.previous_state = previous_state
        self.new_state = new_state


