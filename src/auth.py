from controllers.usersController import handleNewUser, handleFindEmail, handleFindUser, handleFetchUser
from flask import request, Blueprint, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from src.constants.http_status_code import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_406_NOT_ACCEPTABLE, HTTP_405_METHOD_NOT_ALLOWED
from flask_jwt_extended import create_access_token
import validators
import string
import random

auth = Blueprint("auth", __name__, url_prefix="/api/v1/auth")

# generate token


def generate_token():
    token = ""
    # create string of characters
    characters = string.ascii_lowercase+string.digits + \
        string.ascii_uppercase+string.octdigits+"€#¢@£%^&*"

    token = "".join(random.choice(characters) for k in range(30))

    return "0xff"+token


# sign up route
@auth.route("/create/user", methods=["POST"])
def create_user():

    # get variables from json post
    name = request.json.get("Full-name", "")
    email = request.json.get("Email", "")
    phone = request.json.get("Phone", "")
    username = request.json.get("Username", "")
    pwd = request.json.get("Password", "")
    pwd2 = request.json.get("Confirm_password", "")

    # strip white space
    name = name.strip()
    email = email.strip()
    phone = phone.strip()
    username = username.strip()

    # initialize return data
    data = {}
    status = False
    message = ""

    # if request is a post
    if request.method == "POST":
        # check for name empty data
        if name == "":
            message = "Empty full name field"
            return jsonify({"status": status, "message": message, "data": data}), HTTP_400_BAD_REQUEST
        # check for phone empty data
        if phone == "":
            message = "Empty phone number field"
            return jsonify({"status": status, "message": message, "data": data}), HTTP_400_BAD_REQUEST
        # check for username empty data
        if username == "":
            message = "Empty username field"
            return jsonify({"status": status, "message": message, "data": data}), HTTP_400_BAD_REQUEST
        # check if password is empty
        if pwd == "":
            message = "empty password field"
            return jsonify({"status": status, "message": message, "data": data}), HTTP_400_BAD_REQUEST
        # check if email is empty
        if email == "":
            message = "empty email field"
            return jsonify({"status": status, "message": message, "data": data}), HTTP_400_BAD_REQUEST

        # check if it's full name
        if not " " in name:
            message = "enter name with space seperator"
            return jsonify({"status": status, "message": message, "data": data}), HTTP_400_BAD_REQUEST
        # check if it's valid email
        if not validators.email(email):
            message = "invalid email address"
            return jsonify({"status": status, "message": message, "data": data}), HTTP_400_BAD_REQUEST
        # check if valid phone number
        # if len(phone) != 11:
        #     message = "invalid phone number"
        #     return jsonify({"status": status, "message": message, "data": data}), HTTP_400_BAD_REQUEST
        # check username lenght
        if len(username) < 4:
            message = "username too short, must be greater than 4 characters"
            return jsonify({"status": status, "message": message, "data": data}), HTTP_400_BAD_REQUEST
        # check password lenght
        if len(pwd) < 7:
            message = "password too short, must be greater than 7 characters"
            return jsonify({"status": status, "message": message, "data": data}), HTTP_400_BAD_REQUEST
        # check if password matches
        if pwd != pwd2:
            message = "incorrect password"
            return jsonify({"status": status, "message": message, "data": data}), HTTP_400_BAD_REQUEST

        # validate email and username from db
        chk_email = handleFindEmail(email)

        if chk_email is not None:
            message = "email already exit"
            return jsonify({"status": status, "message": message, "data": data}), HTTP_406_NOT_ACCEPTABLE

        # validate if username exit
        chk_email = handleFindUser(username)

        if chk_email is not None:
            message = "username already exit"
            return jsonify({"status": status, "message": message, "data": data}), HTTP_406_NOT_ACCEPTABLE

        # hash password
        hash_pwd = generate_password_hash(pwd)
        user_token = generate_token()

        # call handle new user function

        handleNewUser(name, email, phone, username, user_token, hash_pwd)

        # create data response
        data = {"Name": name, "Email": email, "Phone": phone, "Username": username,
                "Balance": 2.0, "Address": user_token, "Transactions": [], "Cart": []}

        # set status to true
        status = True

    else:
        message = "The method is not allowed for the requested URL."
        return jsonify({"status": status, "message": message, "data": data}), HTTP_405_METHOD_NOT_ALLOWED

    return jsonify({"status": status, "message": message, "data": data}), HTTP_200_OK


# login route
@auth.route("/login/user", methods=["POST"])
def login_user():

    # initialize return data
    data = {}
    status = False
    message = ""

    if request.method == "POST":

        # get json post request
        emailorusername = request.json.get("User", "")
        pwd = request.json.get("Password", "")

        emailorusername = emailorusername.strip()
        pwd = pwd.strip()

        # check if empty username/email password
        if emailorusername == "":
            message = "Empty username/email field"
            return jsonify({"status": status, "message": message, "data": data}), HTTP_406_NOT_ACCEPTABLE

        if pwd == "":
            message = "Empty password field"
            return jsonify({"status": status, "message": message, "data": data}), HTTP_406_NOT_ACCEPTABLE

        # if user enter email, login with emil
        user = None

        # check if user exit
        if validators.email(emailorusername):
            user = handleFindEmail(emailorusername)
        else:
            user = handleFindUser(emailorusername)

        # user doesnt exit
        if user is None:
            message = "user doesn't exit, username is case sensitive"
            return jsonify({"status": status, "message": message, "data": data}), HTTP_406_NOT_ACCEPTABLE

        # confirm password
        chk_pwd = check_password_hash(password=pwd, pwhash=user["Password"])

        if not chk_pwd:
            message = "Incorrect password"
            return jsonify({"status": status, "message": message, "data": data}), HTTP_406_NOT_ACCEPTABLE

        # return data
        data = {"Address": user["Address"], "Name": user["Name"], "Email": user["Email"],
                "Phone": user["Phone"], "Username": user["Username"], "LastScan": user["LastScan"]}

        status = True

    else:
        message = "The method is not allowed for the requested URL."
        return jsonify({"status": status, "message": message, "data": data}), HTTP_405_METHOD_NOT_ALLOWED

    return jsonify({"status": status, "message": message, "data": data}), HTTP_200_OK


# me route
@auth.route("/me", methods=["POST"])
def me():

    # initialize return data
    data = {}
    status = False
    message = ""

    if request.method == "POST":

        # get json post request
        username = request.json.get("Username", "")

        username = username.strip()

        user = handleFetchUser(username)

        # user doesnt exit
        if user is None:
            message = "user doesn't exit, username is case sensitive"
            return jsonify({"status": status, "message": message, "data": data}), HTTP_406_NOT_ACCEPTABLE

        # return data
        data = {"Address": user["Address"], "Name": user["Name"], "Email": user["Email"],
                "Phone": user["Phone"], "Username": user["Username"], "LastScan": user["LastScan"]}

        status = True

    else:
        message = "The method is not allowed for the requested URL."
        return jsonify({"status": status, "message": message, "data": data}), HTTP_405_METHOD_NOT_ALLOWED

    return jsonify({"status": status, "message": message, "data": data}), HTTP_200_OK
