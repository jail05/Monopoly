from ..DS.Tree import Tree
from enum import Enum, auto
from ..DS.stack import Stack
from .card import CardEffectType
from .action import *

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

        # این همون undoStack هست
        self.action_history = Stack(100)
        self.redo_stack = Stack(100)
        self.number_of_get_out_of_jail_card = 0
        self.house_count_for_repair = 0
        self.hotel_count_for_repair = 0

    def move(self,amount):
        if self.state == PlayerState.ACTIVE:
            for i in range(amount):
                self.current_tile = self.current_tile.next


    def pay(self, amount):
        if not self.ability_to_pay(amount):
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
        property.house_counter()
        self.house_count_for_repair += 1

    def build_hotel(self,property):
        property.has_hotel()
        self.hotel_count_for_repair +=1

    def go_to_jail(self):
        self.jail_turns += 1
        self.state = PlayerState.IN_JAIL

    def leave_jail(self):
        self.jail_turns -= 1
        self.state = PlayerState.CURRENT_TURN

    def Use_get_out_of_jail_card(self):
        if self.number_of_get_out_of_jail_card == 0:
            return False
        self.state = PlayerState.CURRENT_TURN
        return True



    def can_trade(self, give_money, give_properties):
        if self.balance< give_money:
            return False
        if give_properties :
            for property in give_properties:
                if property.owner_id != self.id and property.is_mortgaged():
                    return False
        return True

    def propose_trade(self, other_player, give_money=0, give_properties=None, take_money=0, take_properties=None):
        if give_properties is None:
            give_properties = []
        if take_properties is None:
            take_properties = []
        if not self.can_trade(give_money, give_properties):
            return False
        if not other_player.can_trade(take_money, take_properties):
            return False
        self.execute_trade(other_player, give_money, give_properties, take_money, take_properties)
        return True

    def execute_trade(self, other_player, give_money, give_properties, take_money, take_properties):
        self.balance -= give_money
        other_player.balance += give_money

        other_player.balance -= take_money
        self.balance += take_money


        for prop in give_properties:
            prop.owner_id = other_player.id
            self.own_properties.delete(prop)
            other_player.own_properties.insert(prop)

        for prop in take_properties:
            prop.owner_id = self.id
            other_player.own_properties.delete(prop)
            self.own_properties.insert(prop)


        action = Action(self.id,ActionType.Trade)
        action.affected_entities = [other_player.id]
        self.action_history.push(action)

    def get_card(self,chance):
        return chance.get_card()

    def apply_card_effect(self,card):
        if card.effect_type == CardEffectType.MOVE:
            self.move(card.effect_value)
        elif card.effect_type == CardEffectType.PAY_MONEY:
            done = self.pay(card.effect_value)
        elif card.effect_type == CardEffectType.RECEIVE_MONEY:
            self.recieve(card.effect_value)
        elif card.effect_type == CardEffectType.GO_TO_JAIL:
            self.go_to_jail()
        elif card.effect_type == CardEffectType.GET_OUT_OF_JAIL:
            self.number_of_get_out_of_jail_card +=1
        elif card.effect_type == CardEffectType.REPAIR:
            self.pay(self.hotel_count_for_repair*card.effect_value*3 + self.house_count_for_repair*card.effect_value)

    def add_action(self,action):
        self.action_history.push(action)
        self.redo_stack.empty()

    def undo_action(self):
        if self.action_history.isEmpty():
            print("ops! No action to undo")
            return
        action = self.action_history.pop()
        self.apply_state(action.previous_state)
        self.redo_stack.push(action)

    def redo_action(self):
        if self.redo_stack.isEmpty():
            print("ops! No action to redo")
            return
        action = self.redo_stack.pop()
        self.apply_state(action.new_state)
        self.action_history.push(action)

    def apply_state(self,state):
        self.balance = state["balance"]
        self.current_tile = state["current_tile"]
        self.state = state["player_state"]
        self.jail_turns = state["jail_turns"]
        self.own_properties = state["own_properties"]










