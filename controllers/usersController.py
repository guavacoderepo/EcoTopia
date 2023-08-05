from src.modules.mongodb import mongo
from datetime import datetime

# init
db = mongo

def handleNewUser(name, email, phone, username, token, hash_pwd):
    # return new user date
    return db.users.insert_one(
        {   
            "Name": name,
            "Email": email,
            "Phone": phone,
            "Username": username,
            "Password": hash_pwd,
            "Balance": 2.0,
            "Address": token,
            "Transactions": [],
            "Cart": [],
            "LastScan": datetime.now(),
            "created_at": datetime.now()
        }
    )

def handleFetchUser(username):
    return db.users.find_one({"Username": username})

# user find section
def handleFindUser(username):
    return db.users.find_one({"Username": username})

def handleFindEmail(email):
    return db.users.find_one({"Email": email})

def handleUpdateuUser(user, coin):
    return db.users.update_one({"Username": user}, {
        "$set": {
            "Balance": coin,
            "LastScan": datetime.now(),
        },
    })
