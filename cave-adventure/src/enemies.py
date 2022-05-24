class Enemy:
    def __str__(self):
        return self.name

    def is_alive(self):
        return self.hp > 0


class GiantSpider(Enemy):
    def __init__(self):
        self.name = " Giant Spider"
        self.hp = 1 # 10 
        self.damage = 2


class Ogre(Enemy):
    def __init__(self):
        self.name = "Ogre"
        self.hp = 1 # 30
        self.damage = 10


class BatColony(Enemy):
    def __init__(self):
        self.name = "Colony of Bats"
        self.hp = 1 # 100
        self.damage = 4


class RockMonster(Enemy):
    def __init__(self):
        self.name = "Rock Monster"
        self.hp = 1 # 80
        self.damage = 15
