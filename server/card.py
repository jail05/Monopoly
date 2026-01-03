from enum import Enum, auto


class CardEffectType(Enum):
    MOVE = auto()
    PAY_MONEY = auto()
    RECEIVE_MONEY = auto()
    GO_TO_JAIL = auto()
    GET_OUT_OF_JAIL = auto()
    REPAIR = auto()


class Card:
    ID = 0
    def __init__(self,description, effect_type, effect_value):
        Card.ID += 1
        self.card_id = Card.ID
        self.description = description
        self.effect_type = effect_type
        self.effect_value = effect_value


