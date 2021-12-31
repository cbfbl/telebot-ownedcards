import os
import random
from flask import (
    Flask,
    request,
)
import telebot
from constants import API_KEY, MAXIMUM_NUMBER_OF_SUGGESTED_RESULTS
from db_controller import CardsMongoDB

bot = telebot.TeleBot(API_KEY)
cards_db = CardsMongoDB()
server = Flask(__name__)

@bot.message_handler(commands=["Psol"])
def g(message):
    bot.reply_to(message, "Psolss")

@bot.message_handler(commands=["search", "Search"])
def find_card(message):
    message_words = message.text.split()

    if len(message_words) < 2:
        bot.send_message(message.chat.id, "Please enter a valid format of /search <cardname>")
        return
    
    searched_card_name = ' '.join(message_words[1:])

    card = cards_db.find_card_in_db(searched_card_name)
    if card:
        bot.reply_to(message, f"Have {searched_card_name} in the collection :)")
        bot.send_photo(message.chat.id, card["Image URL"])
        return

    close_enough_cards = cards_db.find_similar_cards_names(searched_card_name)

    if close_enough_cards:
        number_of_suggested_results = min(MAXIMUM_NUMBER_OF_SUGGESTED_RESULTS, len(close_enough_cards))
        bot.reply_to(message, f"Did not find exact match, showing {number_of_suggested_results} "
                     f"results with simillar name:\n{random.sample(close_enough_cards, k=number_of_suggested_results)}")
        return
    
    bot.reply_to(message, "Sorry could not find any similar cards in the collection :(")


@server.route('/' + API_KEY, methods=['POST'])
def getMessage():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200


@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://telecardbot.herokuapp.com/' + API_KEY)
    return "!", 200


if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))