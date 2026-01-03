from .card import *
from ..DS import quque
from ..DS.quque import Queue


class ChanceCard:
    def __init__(self):
        self.cards = Queue()
        self.createChanceCard()

    def createChanceCard(self):
        c = Card("3 خونه برو جلو!" , CardEffectType.MOVE , 3)
        self.cards.enqueue(c)
        c = Card("10 سکه به بانک بپرداز:(" , CardEffectType.PAY_MONEY, 10)
        self.cards.enqueue(c)
        c = Card("تبریک! 10 سکه برنده شدی:)", CardEffectType.RECEIVE_MONEY, 10)
        self.cards.enqueue(c)
        c = Card("یک دور به زندان برو! وقت استراحته:)", CardEffectType.GO_TO_JAIL, 1)
        self.cards.enqueue(c)
        c = Card("می‌تونی از این کارت برای ییچوندن یه دور زندان استفاده کنی. نگهش دار لازمت میشه!", CardEffectType.GET_OUT_OF_JAIL, 1)
        self.cards.enqueue(c)
        c = Card("شما که سرمایه داری;)حالا یه 5دلار به ازای هر خونه‌ت مالیات بده", CardEffectType.REPAIR, 5)
        self.cards.enqueue(c)
        c = Card("4خونه عقب گرد کن:]", CardEffectType.MOVE, 4)
        self.cards.enqueue(c)
        c = Card("یه 20 دلار نوش جون;)", CardEffectType.RECEIVE_MONEY, 20)
        self.cards.enqueue(c)

    def drawCard(self):
        return  self.cards.dequeue()

    def returnCard(self, card):
        return self.cards.enqueue(card)
