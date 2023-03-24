from src.modules.mongodb import mongo
from datetime import datetime 


# init
db = mongo.EcoTopia


def handleFindToken(token):
    return db.transactions.find_one({"Token": token})


def handleUpdateBalnce(user,balance):
    return db.users.update_one({"Username": user}, {
                        "$set": {"Balance": balance}})


def handleNewTransaction(user, price, token, to):
    return db.transactions.insert_one({"sender":user,"To":to,"Amount":price,"Token":token,"created_at":datetime.now()})


def handleUpdateTranscation(user, transactions):
    return db.users.update_one({"Username": user}, {
                        "$set": {"Transactions": transactions}, })





