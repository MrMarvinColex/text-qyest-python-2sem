import copy
import telebot
import src.player as playerlib
from telebot import types
import src.world as world
from src.player import Player as Player
from collections import OrderedDict


bot = telebot.TeleBot("5333812218:AAH7vY6iKTXQms8uu7Ony_SYI0j3Hv66H2I")

@bot.message_handler(content_types=['text'])
def play(message):
    bot.send_message(message.from_user.id, "Escape from Cave Terror!")
    bot.send_message(message.from_user.id, "Your message is " + message.text)
    world.parse_world_dsl()
    player = Player(bot, message)
    player.message = message
    while player.is_alive() and not player.victory:
        room = world.tile_at(player.x, player.y)
        bot.send_message(message.from_user.id, room.intro_text())
        room.modify_player(player, bot, message)
        if player.is_alive() and not player.victory:
            choose_action(message, room, player)
        elif not player.is_alive():
            bot.send_message(message.from_user.id, "Your journey has come to an early end!")


def get_available_actions(room, player, message):
    actions = OrderedDict()
    keyboard = types.InlineKeyboardMarkup();
    if player.inventory:
        keyWord = 'i'
        action_adder(actions, 'i', player.print_inventory, "Print inventory", message)
        key_i = types.InlineKeyboardButton(text=keyWord, callback_data=keyWord)
        keyboard.add(key_i)
    if isinstance(room, world.TraderTile):
        keyWord = 't'
        action_adder(actions, 't', player.trade, "Trade", message)
        key_t = types.InlineKeyboardButton(text=keyWord, callback_data=keyWord)
        keyboard.add(key_t)
    if isinstance(room, world.EnemyTile) and room.enemy.is_alive():
        keyWord = 'a'
        action_adder(actions, 'a', player.attack, "Attack", message)
        key_a = types.InlineKeyboardButton(text=keyWord, callback_data=keyWord)
        keyboard.add(key_a)
    else:
        if world.tile_at(room.x, room.y - 1):
            keyWord = 'n'
            action_adder(actions, 'n', player.move_north, "Go North", message)
            key_n = types.InlineKeyboardButton(text=keyWord, callback_data=keyWord)
            keyboard.add(key_n)
        if world.tile_at(room.x, room.y + 1):
            keyWord = 's'
            action_adder(actions, 's', player.move_south, "Go South", message)
            key_s = types.InlineKeyboardButton(text=keyWord, callback_data=keyWord)
            keyboard.add(key_s)
        if world.tile_at(room.x + 1, room.y):
            keyWord = 'e'
            action_adder(actions, 'e', player.move_east, "Go East", message)
            key_e = types.InlineKeyboardButton(text=keyWord, callback_data=keyWord)
            keyboard.add(key_e)
        if world.tile_at(room.x - 1, room.y):
            keyWord = 'w'
            action_adder(actions, 'w', player.move_west, "Go West", message)
            key_w = types.InlineKeyboardButton(text=keyWord, callback_data=keyWord)
            keyboard.add(key_w)
        if player.hp < 100:
            keyWord = 'h'
            action_adder(actions, 'h', player.heal, "Heal", message)
            key_h = types.InlineKeyboardButton(text=keyWord, callback_data=keyWord)
            keyboard.add(key_h)

    bot.send_message(message.from_user.id, text="Choose an action:", reply_markup=keyboard)
    return actions


def action_adder(action_dict, hotkey, action, name, message):
    action_dict[hotkey.lower()] = action
    action_dict[hotkey.upper()] = action
    bot.send_message(message.from_user.id, "{} : {}".format(hotkey, name))


def choose_action(message, room, player):
    action = None
    available_actions = get_available_actions(room, player, message)
    global command
    command = None
    while True:
        if command != None:
            break
    action = available_actions.get(command)
    action()

@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    global command
    playerlib.gameCommand = copy.copy(call.data)
    print("World command now is not None")
    world.worldCommand = copy.copy(call.data)
    command = copy.copy(call.data)

command = None
bot.polling(none_stop=True, interval=0)
