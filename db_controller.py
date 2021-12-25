# import pandas
import pymongo
from constants import mongodb_password, magic_data_file

class CardsMongoDB(object):
    def __init__(self):
        client = pymongo.MongoClient(f"mongodb+srv://telebot:{mongodb_password}@cluster0.lqrbk.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
        db = client.magicCards
        self.cards_collection = db.get_collection("magicCards")
        self.cards_collection.create_index("Name")

    # def _populate_db(collection):
    #     magic_cards_data_frame = pandas.read_csv(magic_data_file)
    #     rows_list = [row.to_dict() for _, row in magic_cards_data_frame.iterrows()]
    #     for row_dict in rows_list:
    #         row_dict["Image URL"] = row_dict["Image URL"].split("https://")[2]
    #     collection.insert_many(rows_list)


    def find_card_in_db(self, card_name):
    
        return self.cards_collection.find_one({"Name": card_name})

    def find_similar_cards_names(self, card_name):
    
        return [row["Name"] for row in self.cards_collection.find(projection={"Name": True, "_id": False}) if card_name in row["Name"]]

# print(find_card_in_db("Wilt"))
# print(find_similar_cards_names("Wil"))
# populate_db(cards_collection)
