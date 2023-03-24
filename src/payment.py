from flask import Blueprint, request, jsonify
from controllers.transactions import handleFindToken, handleUpdateBalnce, handleNewTransaction, handleUpdateTranscation
from controllers.usersController import handleFindUser


payment = Blueprint("payment", __name__, url_prefix="/api/v1/payment")

@payment.route("/checkout/", methods = ["POST", "GET"])
def checkout():
    # initialize return data
    data = {}
    status = False
    message = "" 

    # check post request
    if request.method == "POST":
        bank = request.json.get("Bank", "")
        amount = request.json.get("Amount", 0)
        name = request.json.get("Name", "")
        token = request.json.get("Token", "")
        user = request.json.get("Username", "")


         # check if token already exit
        duplicate = handleFindToken(token)
        if duplicate is not  None:
            message = "duplicate transaction"
            return jsonify({"status":status,"message":message,"data":data})

        # check bank length
        if bank == "":
            message = "empty bank selected"
            return jsonify({"status":status,"message":message,"data":data})

        # check name
        if name == "":
            message = "empty name field"
            return jsonify({"status":status,"message":message,"data":data})

        # check address
        if user == "":
            message = "empty address"
            return jsonify({"status":status,"message":message,"data":data})

        # check if address exit
        user = handleFindUser(user)

        if user is None:
            message = "invalid user"
            return jsonify({"status":status,"message":message,"data":data})
        
        balance = user["Balance"]

        # check if amount avaible 
        if amount > balance:
            message = "insuffient balance"
            return jsonify({"status":status,"message":message,"data":data})

        try:
              
            # minus the money from the wallet 
            newBalance = balance - amount
            
            # update balance in users
            handleUpdateBalnce(user,newBalance)

            # add to transactions
            newtransacton = handleNewTransaction(user, amount, token, bank)
            
            # get user transactions
            transactions = user["Transactions"]

            # add transaction to transactions list
            transactions.append(newtransacton.inserted_id)
            
            # update transactons
            handleUpdateTranscation(user,transactions)
            
            # set returen param
            data = {"Amout":amount, "To":bank, "Sender":user["Address"], "Transaction-id":str(newtransacton.inserted_id)}
            status = True

        except:
            message = "an error occured.... please try again"
       


    # check if request is a get
    else:
        message = "This method is not allowed for the requested URL."


    return jsonify({"status":status,"message":message,"data":data})
