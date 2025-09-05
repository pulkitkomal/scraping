import telebot

from src.utils.configs import TELEGRAM_TOKEN, logger
from src.utils.db import mongo
from src.services.scrape import DiecastScraper

bot = telebot.TeleBot(TELEGRAM_TOKEN, parse_mode=None)
logger.info("Started telegram bot !!")


@bot.message_handler(commands=["start", "help"])
def send_welcome(message):
    bot.reply_to(message, "Howdy, how are you doing?")


@bot.message_handler(commands=["collect_info"])
def collect_info(message):
    bot.send_chat_action(message.chat.id, "typing")
    try:
        ds = DiecastScraper()
        bot.send_message(message.chat.id, "Going through the web")
        bot.send_chat_action(message.chat.id, "typing")
        tokens_used = ds.scrape_diecast_info()
        bot.send_message(message.chat.id, "Populating Database")
        bot.send_chat_action(message.chat.id, "typing")
        total_records = ds.write_to_mongo()
        status = f"Collected new info for {len(total_records)} cars, total tokens used: {tokens_used['total_token_used']}, total cost: {tokens_used['total_cost']}"
        if not total_records:
            bot.send_chat_action(message.chat.id, "typing")
            bot.send_message(message.chat.id, "No new cars !!")
        for cars in total_records:
            bot.send_chat_action(message.chat.id, "typing")
            bot.send_message(message.chat.id, f"{cars['website']} -- {cars['car_name']}")

    except Exception as e:
        logger.exception(f"Error: {e}")
        status = f"Error: {e}"
    bot.reply_to(message, status)


@bot.message_handler(commands=["lookup"])
def collect_info(message):
    bot.send_chat_action(message.chat.id, "typing")
    try:
        cars = mongo.read_data_diecast(hours=2)
    except Exception as e:
        logger.exception(f"Error: {e}")
        cars = (f"Error: {e}", None)
    if not cars:
        bot.send_chat_action(message.chat.id, "typing")
        bot.send_message(message.chat.id, "No new cars !!")
    for car, website in cars:
        bot.send_chat_action(message.chat.id, "typing")
        bot.send_message(message.chat.id, f"{website} -- {car}")



@bot.message_handler(func=lambda m: True)
def echo_all(message):
    bot.send_chat_action(message.chat.id, "typing")
    if 'find: ' in message.text:
        cars = message.text.split(' ')
        for input_car in cars[1:]:
            bot.send_chat_action(message.chat.id, "typing")
            bot.send_message(message.chat.id, f"Looking up car {input_car}")
            car_names = mongo.read_individual_car_diecast(name=input_car, minutes=60)
            if not car_names:
                bot.send_chat_action(message.chat.id, "typing")
                bot.send_message(message.chat.id, f"No Car Found expanding search to last 4 hours")
                car_names = mongo.read_individual_car_diecast(name=input_car, minutes=240)
            
            if not car_names:
                bot.send_chat_action(message.chat.id, "typing")
                bot.send_message(message.chat.id, f"No Car Found expanding search to last 12 hours")
                car_names = mongo.read_individual_car_diecast(name=input_car, minutes=720)

            for car, website in car_names:
                bot.send_chat_action(message.chat.id, "typing")
                bot.send_message(message.chat.id, f"{website} -- {car}")
            if not car_names:
                bot.send_chat_action(message.chat.id, "typing")
                bot.send_message(message.chat.id, "No cars found !!")
    else:
        bot.reply_to(message, message.text)

