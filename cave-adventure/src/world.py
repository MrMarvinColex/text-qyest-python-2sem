import src.enemies as enemies
import src.mobs as mobs
import random
from telebot import types


class MapTile:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def modify_player(self, player, bot, message):
        pass


class StartTile(MapTile):
    def intro_text(self):
        return """
        You find yourself in a cave with a flickering torch
        on the wall.
        You can make out four paths, each equally as dark and foreboding.
        """


class BoringTile(MapTile):
    def intro_text(self):
        return """
        This is very boring part of the cave
        """


class VictoryTile(MapTile):
    def intro_text(self):
        return """
        You see a bright light in the distance...
        ... it grows as you get closer! It's sunlight!
        
        
        Victory is yours!
        """

    def modify_player(self, player, message):
        player.victory = True


class EnemyTile(MapTile):
    def __init__(self, x, y):
        r = random.random()
        if r < 0.50:
            self.enemy = enemies.GiantSpider()
            self.alive_text = "A giant Spider jumps down from " \
                              "its web in front of you!"
            self.dead_text = "The corpse of a dead spider rots on " \
                             "the ground."
        elif r < 0.80:
            self.enemy = enemies.Ogre()
            self.alive_text = "A Ogre is blocking your path "
            self.dead_text = "A dead Ogre reminds you of your triumph."
        elif r < 0.95:
            self.enemy = enemies.BatColony()
            self.alive_text = "You hear a squeaking noise growing louder" \
                              "...suddenly you are lost in a swarm of bats!"
            self.dead_text = "Dozens of dead bats are scattered on the ground"
        else:
            self.enemy = enemies.RockMonster()
            self.alive_text = "You have disturbed a rock monster from his slumber! "
            self.dead_text = "Defeated, the monster has reverted into an ordinary rock"

        super().__init__(x, y)

    def intro_text(self):
        text = self.alive_text if self.enemy.is_alive() else self.dead_text
        return text

    def modify_player(self, player, bot, message):
        if self.enemy.is_alive():
            player.hp = player.hp - self.enemy.damage
            bot.send_message(message.from_user.id, "Enemy does {} damage. You have {} HP remaining."
                  .format(self.enemy.damage, player.hp))


class TraderTile(MapTile):
    def intro_text(self):
        return """
        A Frail not-quite-human, not-quite-creature squats in
        the corner
        clinking his gold coins together. He looks willing to 
        trade.
        """

    def __init__(self,x,y):
        self.trader = mobs.WanderingTrader()
        super().__init__(x, y)

    def trade(self, buyer, seller, bot, message):
        global worldCommand
        keyboard = types.InlineKeyboardMarkup();
        key_i = types.InlineKeyboardButton(text='Q', callback_data='Q')
        keyboard.add(key_i)
        
        for i, item in enumerate(seller.inventory, 1):
            key_i = types.InlineKeyboardButton(text=i, callback_data=i)
            keyboard.add(key_i)
            bot.send_message(message.from_user.id, "{}. {} - {} Gold".format(i, item.name, item.value))
        
        while True:
            worldCommand = None
            bot.send_message(message.from_user.id, "Choose an item or press Q to exit: ", reply_markup=keyboard)
            
            # worldCommand определяется в общей функции, ловящей все сообщения, в "game.py"
            while True:
                if worldCommand != None:
                    break
            
            user_input = worldCommand
            if user_input in ['Q', 'q']:
                return
            else:
                try:
                    choice = int(user_input)
                    to_swap = seller.inventory[choice - 1]
                    self.swap(seller, buyer, to_swap, bot, message)
                except:
                    bot.send_message(message.from_user.id, "Invalid choice!")
    
    def swap(self, seller, buyer, item, bot, message):
        if item.value > buyer.gold:
            bot.send_message(message.from_user.id, "That's too expensive")    
            return
        seller.inventory.remove(item)
        buyer.inventory.append(item)
        seller.gold = seller.gold + item.value
        buyer.gold = buyer.gold - item.value
        bot.send_message(message.from_user.id, "Trade completed!")

    def check_if_trade(self, player, bot, message):
        while True:
            global worldCommand
            worldCommand = None
            keyboard = types.InlineKeyboardMarkup();
            key_b = types.InlineKeyboardButton(text='B', callback_data='B')
            keyboard.add(key_b)
            key_s = types.InlineKeyboardButton(text='S', callback_data='S')
            keyboard.add(key_s)
            key_q = types.InlineKeyboardButton(text='Q', callback_data='Q')
            keyboard.add(key_q)
            bot.send_message(message.from_user.id, "Would you like to (B)uy, (S)ell, or (Q)uit?", reply_markup=keyboard) 
            
            while True:
                if worldCommand != None:
                    break
            
            user_input = worldCommand
            if user_input in ['q', 'Q']:
                return
            elif user_input in ['B', 'b']:
                bot.send_message(message.from_user.id, "Here's whats available to buy: ")
                self.trade(player, self.trader, bot, message)
            elif user_input in ['S', 's']:
                bot.send_message(message.from_user.id, "Here's whats available to sell: ")
                self.trade(self.trader, player, bot, message)
            else:
                bot.send_message(message.from_user.id, "Invalid choice!")


class FindGoldTile(MapTile):
    def __init__(self, x, y):
        self.gold = random.randint(1, 50)
        self.gold_claimed = False
        super().__init__(x, y)


    def modify_player(self, player, bot, message):
        if not self.gold_claimed:
            self.gold_claimed = True
            player.gold = player.gold + self.gold
            bot.send_message(message.from_user.id, "+{} gold added.".format(self.gold))


    def intro_text(self):
        if self.gold_claimed:
            return"""
            Another unremarkable part of the cave.
            You must forge onward.
            """
        else:
            return"""
            Someone dropped some gold. You pick it up.
            """


def is_dsl_valid(dsl):
    if dsl.count("|ST|") != 1:
        return False
    
    if dsl.count("|VT|") == 0:
        return False
    
    lines = dsl.splitlines()
    lines = [l for l in lines if l]
    pipe_counts = [line.count("|") for line in lines]
    for count in pipe_counts:
        if count != pipe_counts[0]:
            return False

    return True


def parse_world_dsl():
    dsl_lines = world_dsl.splitlines()
    dsl_lines = [x for x in dsl_lines if x]

    for y, dsl_row in enumerate(dsl_lines):
        row = []
        dsl_cells = dsl_row.split("|")
        dsl_cells = [c for c in dsl_cells if c]
        for x, dsl_cell in enumerate(dsl_cells):
            tile_type = tile_type_dict[dsl_cell]
            
            if tile_type == StartTile:
                global start_tile_location
                start_tile_location = x, y
            
            row.append(tile_type(x, y) if tile_type else None)

        world_map.append(row)


def tile_at(x, y):
    if x < 0 or y < 0:
        return None
    try:
        return world_map[y][x]
    except IndexError:
        return None


world_dsl = """
|EN|EN|VT|EN|EN|
|EN|EN|  |  |EN|
|EN|  |EN|EN|TT|
|TT|  |ST|FG|EN|
|FG|  |EN|  |FG|
"""

world_map = []

tile_type_dict = {"VT": VictoryTile,
                  "EN": EnemyTile,
                  "ST": StartTile,
                  "FG": FindGoldTile,
                  "TT": TraderTile,
                  "  ": None}

start_tile_location = None
worldCommand = None
