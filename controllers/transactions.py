from src.modules.mongodb import mongo

# init
db = mongo.EcoTopia


def handleFindToken(token):
    return db.transactions.find_one({"Token": token})


