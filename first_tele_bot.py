import pandas
import random
import telebot
from constants import API_KEY, magic_data_file, MAXIMUM_NUMBER_OF_SUGGESTED_RESULTS

bot = telebot.TeleBot(API_KEY)

@bot.message_handler(commands=["Psol"])
def g(message):
    bot.reply_to(message, "Psolss")

@bot.message_handler(commands=["search", "Search"])
def find_card(message):
    magic_cards_data_frame = pandas.read_csv(magic_data_file, index_col="Name")
    message_words = message.text.split()

    if len(message_words) < 2:
        bot.send_message(message.chat.id, "Please enter a valid format of /search <cardname>")
        return
    searched_card_name = message_words[1]
    
    if searched_card_name in magic_cards_data_frame.index:
        bot.reply_to(message, f"Have {searched_card_name} in the collection :)")
        bot.send_photo(message.chat.id, magic_cards_data_frame.loc[searched_card_name, "Image URL"].split("https://")[2])
        return

    close_enough_cards = list(magic_cards_data_frame.filter(like=searched_card_name, axis=0).index.values)
    if len(close_enough_cards):
        number_of_suggested_results = min(MAXIMUM_NUMBER_OF_SUGGESTED_RESULTS, len(close_enough_cards))
        bot.reply_to(message, f"Did not find exact match, showing {number_of_suggested_results} "
                     f"results with simillar name:\n{random.sample(close_enough_cards, k=number_of_suggested_results)}")
        return
    
    bot.reply_to(message, "Sorry could not find any similar cards in the collection :(")


bot.polling()