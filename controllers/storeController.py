from src.modules.mongodb import mongo
from datetime import datetime

# init
db = mongo

def handleNewStoreItem(description, category, title, price, quantity, img_url):
    return db.store.insert_one({"Description": description, "Category": category, "Title": title, "Price": price, "Quantity": quantity, "ImgUrl": img_url, "Created_at": datetime.now()})

def handleFetchStoreItems():
    return db.store.find()
