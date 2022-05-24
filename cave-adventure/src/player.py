import src.items as items
import src.world as world
import telebot
from telebot import types


bot = telebot.TeleBot("PASTE TOKEN HERE")

class Player:
    def __init__(self, bot, message):
        self.inventory = [items.ShardOfGlass(),
                          items.ShardOfGlass(),
                          items.Knife(),
                          items.AppleOfDetermination(),
                          items.AppleOfDetermination()]

        self.x = world.start_tile_location[0]
        self.y = world.start_tile_location[1]
        self.hp = 100
        self.gold = 0
        self.victory = False
        self.bot = bot
        self.message = message

    def is_alive(self):
        return self.hp > 0

    # here
    def print_inventory(self):
        self.bot.send_message(self.message.from_user.id, "Inventory:")
        for item in self.inventory:
            self.bot.send_message(self.message.from_user.id, "*" + str(item))
        self.bot.send_message(self.message.from_user.id, "*Gold : {}".format(self.gold))
        best_weapon = self.most_powerful_weapon()
        self.bot.send_message(self.message.from_user.id, "Your best weapon is your {}".format(best_weapon))

    def most_powerful_weapon(self):
        max_damage = 0
        best_weapon = None

        for item in self.inventory:
            try:
                if item.damage > max_damage:
                    best_weapon = item
                    max_damage = item.damage
            except AttributeError:
                pass

        return best_weapon

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def move_north(self):
        self.move(dx=0, dy=-1)

    def move_south(self):
        self.move(dx=0, dy=1)

    def move_east(self):
        self.move(dx=1, dy=0)

    def move_west(self):
        self.move(dx=-1, dy=0)

    # here
    def attack(self):
        best_weapon = self.most_powerful_weapon()
        room = world.tile_at(self.x, self.y)
        enemy = room.enemy
        self.bot.send_message(self.message.from_user.id, "You can use {} against!".format(best_weapon.name, enemy.name))
        enemy.hp -= best_weapon.damage
        if not enemy.is_alive():
            self.bot.send_message(self.message.from_user.id, "You killed {}!".format(enemy.name))
        else:
            self.bot.send_message(self.message.from_user.id, "{} HP is {}.".format(enemy.name, enemy.hp))
    
    # here
    def heal(self):
        keyboard = types.InlineKeyboardMarkup();
        heals = [item for item in self.inventory if isinstance(item, items.Healing)]
        if not heals:
            self.bot.send_message(self.message.from_user.id, "You don't have any items to heal you!")
            return

        for i, item in enumerate(heals,1):
            # self.bot.send_message(self.message.from_user.id, "Choose an item to use to heal: ")
            self.bot.send_message(self.message.from_user.id, "{}. {}".format(i, item))
            key_i = types.InlineKeyboardButton(text=i, callback_data=i)
            keyboard.add(key_i)

        self.bot.send_message(self.message.from_user.id, text="Choose:", reply_markup=keyboard)
        valid = False
        global gameCommand
        while not valid:
            while True:
                try:
                    a = int(gameCommand)
                    break
                except:
                    continue
            choice = gameCommand
            to_eat = heals[int(choice) - 1]
            self.hp = min(100, self.hp + to_eat.healing_value)
            self.inventory.remove(to_eat)
            self.bot.send_message(self.message.from_user.id, "Current HP: {}".format(self.hp))
            valid = True
            gameCommand = None


    def trade(self):
        room = world.tile_at(self.x, self.y)
        room.check_if_trade(self, self.bot, self.message)


gameCommand = None
