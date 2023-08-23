import pymongo
import os

MONGO_URI = os.environ["MONGO_URI"]
client = pymongo.MongoClient(MONGO_URI)
db = client["scraper_db"]
collection = db["halooglasi_stanovi"]


def check_if_exists(url):
    return collection.count_documents({"url": url}) > 0


def insert_property(url, price, name, location):
    collection.insert_one({"url": url, "price": price, "name": name, "location": location})
