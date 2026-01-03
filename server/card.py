from enum import Enum, auto


class CardEffectType(Enum):
    MOVE = auto()
    PAY_MONEY = auto()
    RECEIVE_MONEY = auto()
    GO_TO_JAIL = auto()
    GET_OUT_OF_JAIL = auto()
    REPAIR = auto()


class Card:
    def __init__(self, card_id, description, effect_type, effect_value):
        self.card_id = card_id
        self.description = description
        self.effect_type = effect_type
        self.effect_value = effect_value


