from flask import request, Blueprint, jsonify
from src.constants.http_status_code import HTTP_200_OK, HTTP_400_BAD_REQUEST 
from controllers.usersController import handleFetchUser

profile =  Blueprint("profile",__name__,url_prefix="/api/v1/profile")


@profile.route("/",methods = ["POST", "GET"])
def users():
    # init methods
    message = ""
    data = {}
    status = False

    if request.method == "POST":
        user = request.json.get("Username","")

        if user == "":
            message = "empty username"
            return jsonify({"status":status, "message":message, "data":data }),HTTP_400_BAD_REQUEST

        # fetch all users
        user = handleFetchUser(user)

        # get user data
        data = {"Name":user["Name"],"Email":user["Email"],"Phone":user["Phone"],"Username":user["Username"], "Address":user["Address"], "_id":str(user["_id"]), "Cart":user["Cart"],"Balance":user["Balance"]}
        status = True
       
    
    return jsonify({"status":status, "message":"", "data":data }),HTTP_200_OK