import pandas
import pymongo
from constants import mongodb_password, magic_data_file

client = pymongo.MongoClient(f"mongodb+srv://telebot:{mongodb_password}@cluster0.lqrbk.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = client.magicCards
cards_collection = db.get_collection("magicCards")
cards_collection.create_index("Name")

def populate_db(collection):
    magic_cards_data_frame = pandas.read_csv(magic_data_file)
    rows_list = [row.to_dict() for _, row in magic_cards_data_frame.iterrows()]
    for row_dict in rows_list:
        row_dict["Image URL"] = row_dict["Image URL"].split("https://")[2]
    collection.insert_many(rows_list)


def find_card_in_db(card_name):
    
    return cards_collection.find_one({"Name": card_name})

def find_similar_cards(card_name):
    similar_cards = []
    for row in cards_collection.find():
        if card_name in row["Name"]:
            similar_cards.append(row)
    return similar_cards

# print(find_similar_cards("Wil"))
# populate_db(cards_collection)
