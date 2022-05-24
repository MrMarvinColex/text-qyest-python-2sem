import src.items as items
import random


class PassiveMob():
    def __str__(self):
        return self.name


class WanderingTrader(PassiveMob):
    def __init__(self):
        self.name = "Trader"
        self.gold = 70 + random.random() * 60
        self.inventory = [items.GingerCookies(),
                          items.GingerCookies(),
                          items.GingerCookies(),
                          items.GingerCookies(),
                          items.AppleOfDetermination(),
                          items.AppleOfDetermination(),
                          items.AppleOfDetermination(),
                          items.HealingPotion()]
