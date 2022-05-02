import telebot
import src.world as world


bot = telebot.TeleBot("5333812218:AAH7vY6iKTXQms8uu7Ony_SYI0j3Hv66H2I")

@bot.message_handler(content_types=['text'])
def get_text_messages(message, something=0):
    startTile = world.StartTile(0, 0)
    if message.text == "Привет":
        bot.send_message(message.from_user.id, startTile.intro_text())
        # get_parrot(message)
        bot.register_next_step_handler(message, get_parrot)
    elif message.text == "/help":
        bot.send_message(message.from_user.id, "Напиши привет")
    else:
        bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")

def get_parrot(message):
    bot.send_message(message.from_user.id, message.text)
    bot.register_next_step_handler(message, get_parrot)

bot.polling(none_stop=True, interval=0)
