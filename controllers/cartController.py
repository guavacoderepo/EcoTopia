from src.modules.mongodb import mongo 


# init
db = mongo.EcoTopia

def handleUpdateCart(user,cartlist):
    db.users.update_one({"Username":user}, {"$set":{"Cart":cartlist}})


def handleFindItem(itemid):
    return db.store.find_one({"_id":itemid})

def handleCartPayment():
    pass
