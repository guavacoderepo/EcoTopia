from src.modules.mongodb import mongo
from datetime import datetime 


# init
db = mongo.EcoTopia


def handleFindToken(token):
    return db.transactions.find_one({"Token": token})


def handleUpdateBalnce(user,balance):
    db.users.update_one({"Username": user}, {
                        "$set": {"Balance": balance}})


def handleNewTransaction(user, price, token):
    return db.transactions.insert_one({"sender":user,"To":"Store","Amount":price,"Token":token,"created_at":datetime.now()})


def handleUpdateTranscation(user, transactions):
    db.users.update_one({"Username": user}, {
                        "$set": {"Transactions": transactions}, })





