from src.modules.mongodb import mongo 
from datetime import datetime 

# init
db = mongo.EcoTopia

def handleNewUser(name,email,phone,username,token, hash_pwd):
    # return new user date
    db.users.insert_one({"Name":name,
                            "Email":email,
                            "Phone":phone,
                            "Username":username,
                            "Password":hash_pwd,
                            "Balance":0.0,
                            "Address":token,
                            "Transactions":[], 
                            "Cart":[], 
                            "LastScan":datetime.now(), 
                            "created_at":datetime.now()
                        })
    

def handleUpdateUser():
     # init
    db = mongo.EcoTopia







# user find section
def handleFindUser(username):
    return db.users.find_one({"Username":username})


def handleFindEmail(email):
    return db.users.find_one({"Email":email})


