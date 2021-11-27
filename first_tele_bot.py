import random
import telebot
from constants import API_KEY, MAXIMUM_NUMBER_OF_SUGGESTED_RESULTS
from db_controller import find_card_in_db, find_similar_cards

bot = telebot.TeleBot(API_KEY)

@bot.message_handler(commands=["Psol"])
def g(message):
    bot.reply_to(message, "Psolss")

@bot.message_handler(commands=["search", "Search"])
def find_card(message):
    message_words = message.text.split()

    if len(message_words) < 2:
        bot.send_message(message.chat.id, "Please enter a valid format of /search <cardname>")
        return
    
    searched_card_name = message_words[1]

    card = find_card_in_db(searched_card_name)
    if card:
        bot.reply_to(message, f"Have {searched_card_name} in the collection :)")
        bot.send_photo(message.chat.id, card["Image URL"])
        return

    close_enough_cards = [card["Name"] for card in find_similar_cards(searched_card_name)]

    if len(close_enough_cards):
        number_of_suggested_results = min(MAXIMUM_NUMBER_OF_SUGGESTED_RESULTS, len(close_enough_cards))
        bot.reply_to(message, f"Did not find exact match, showing {number_of_suggested_results} "
                     f"results with simillar name:\n{random.sample(close_enough_cards, k=number_of_suggested_results)}")
        return
    
    bot.reply_to(message, "Sorry could not find any similar cards in the collection :(")

bot.polling()