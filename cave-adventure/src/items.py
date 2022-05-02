class Weapon:
    def __str__(self):
        return self.name


class ShardOfGlass(Weapon):
    def __init__(self):
        self.name = "ShardOfGlass"
        self.description = "Small in size, but can be dangerous."
        self.damage = 5
        self.value = 2


class Knife(Weapon):
    def __init__(self):
        self.name = "Knife"
        self.description = "He may seem curious, but believe me, he hides a lot of secrets."
        self.damage = 10
        self.value = 12


class SilverSword(Weapon):
    def __init__(self):
        self.name = "Silver Sword"
        self.description = "It fits well in the hand, and its weight is very awesome."
        self.damage = 21
        self.value = 42


class ShabbyBow(Weapon):
    def __init__(self):
        self.name = "Shabby Bow"
        self.description = "He may be old, but he won't let the monsters get too close to you."
        self.damage = 29
        self.value = 45


class Crossbow(Weapon):
    def __init__(self):
        self.name = "Crossbow"
        self.description = "With it, your hands will definitely not get tired,\n and it's very enjoyable to kill monsters."
        self.damage = 51
        self.value = 90


class Healing:
    def __str__(self):
        return "{} (+{} HP)".format(self.name, self.healing_value)


class GingerCookies(Healing):
    def __init__(self):
        self.name = "Ginger Cookies"
        # 5 / 6 = 0.8333
        self.healing_value = 5
        self.value = 6


class AppleOfDetermination(Healing):
    def __init__(self):
        self.name = "Apple of Determination"
        # 14 / 17 = 0.8235
        self.healing_value = 14
        self.value = 17


class HealingPotion(Healing):
    def __init__(self):
        self.name = "Healing Potion"
        # 50 / 61 = 0.8196
        self.healing_value = 50
        self.value = 61
