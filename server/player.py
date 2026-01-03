from ..DS.Tree import Tree
from enum import Enum, auto
from ..DS.stack import Stack
from .card import CardEffectType

class PlayerState(Enum):
    CURRENT_TURN = auto()
    ACTIVE = auto()
    IN_JAIL = auto()
    BANKRUPT = auto()

class Player:
    count = 0
    def __init__(self, name,tile_list):
        self.name = name
        Player.count = Player.count + 1
        self.id = Player.count
        self.balance = 100
        self.current_tile = tile_list.head
        self.own_properties = Tree()
        self.state = PlayerState.ACTIVE
        self.jail_turns = 0
        self.action_history = Stack()

    def move(self,amount):
        if self.state == PlayerState.ACTIVE:
            for i in range(amount):
                self.current_tile = self.current_tile.next()


    def pay(amount, self):
        if self.can_afford(amount):
            self.state = PlayerState.BANKRUPT
            return False
        else:
            self.balance -= amount
            return True

    def recieve(self,amount):
        self.balance += amount

    #مصادره ی املاک بعد از ورشکستگی
    def clear_properties(self):
        self.state = PlayerState.BANKRUPT

    def ability_to_pay(self,amount):
        return self.balance >= amount

    def add_property(self,property_id):
        self.own_properties.insert(property_id)

    def remove_property(self,property_id):
        self.own_properties.delete(property_id)

    def has_property(self,property_id):
        return self.own_properties.find_node(property_id)

    def mortgage(self,property):
        self.balance += property.current_rent()+30
        property.mortgage()

    def unmortgage_property(self,property):
        if self.can_afford(property.current_rent()):
            self.balance += property.current_rent() + 30
            property.unmortgage()
            return True
        else:
            return False

    def build_house(self,property):
        property.plus_count()

    def build_hotel(self,property):
        property.has_hotel()

    def go_to_jail(self):
        self.jail_turns += 1
        self.state = PlayerState.IN_JAIL

    def leave_jail(self):
        self.jail_turns -= 1
        self.state = PlayerState.CURRENT_TURN

    def Use_get_out_of_jail_card(self):
        self.state = PlayerState.CURRENT_TURN

    def propose_trade(other_player, offer, request):
        pass




    def get_card(self,chance):
        return chance.get_card()

    def apply_card_effect(self,card):
        if card.effect_type == CardEffectType.MOVE:
            self.move(card.effect_value)
        elif card.effect_type == CardEffectType.PAY_MONEY:
            pass











