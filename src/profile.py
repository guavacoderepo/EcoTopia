from flask import request, Blueprint, jsonify
from src.constants.http_status_code import HTTP_200_OK, HTTP_400_BAD_REQUEST
from controllers.usersController import handleFetchUser, handleUpdateuUser

profile = Blueprint("profile", __name__, url_prefix="/api/v1/profile")


@profile.route("/", methods=["POST"])
def users():
    # init methods
    message = ""
    data = {}
    status = False

    if request.method == "POST":
        user = request.json.get("Username", "")

        if user == "":
            message = "empty username"
            return jsonify({"status": status, "message": message, "data": data}), HTTP_400_BAD_REQUEST

        # fetch all users
        user = handleFetchUser(user)
        try:
            # get user data
            data = {"Name": user["Name"], "Email": user["Email"], "Phone": user["Phone"], "Username": user["Username"], "Address": user["Address"], "_id": str(
                user["_id"]), "Cart": user["Cart"], "Balance": user["Balance"], "lastScan": user["LastScan"]}
            status = True
        except:
            message = "Error getting user profile"
            return jsonify({"status": status, "message": message, "data": data}), HTTP_400_BAD_REQUEST

    return jsonify({"status": status, "message": "", "data": data}), HTTP_200_OK


@profile.route("/update", methods=["GET"])
def update():
    # init methods
    message = ""
    data = {}
    status = False

    if request.method == "GET":
        user = request.args.get("user", "")
        if user == "":
            message = "empty username"
            return jsonify({"status": status, "message": message, "data": data}), HTTP_400_BAD_REQUEST

        # fetch all users

        resuser = handleFetchUser(user)

        try:
            # get user data

            newcoin = float(resuser["Balance"])+2

            handleUpdateuUser(user, newcoin)
            status = True

        except:
            message = "error updating user"
            return jsonify({"status": status, "message": message, }), HTTP_400_BAD_REQUEST

    return jsonify({"status": status, "message": "", "data": data}), HTTP_200_OK
