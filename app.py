# from urllib import request
import code
from API import MongoDB_wrapper, Security, Helper
from flask import Flask, render_template, redirect, request, url_for, session
from pymongo import MongoClient
import json

# Just added gpg to my second laptop let see if this works[#Jacky]


# Web Application name: blue_Jesse
name = "blue_Jesse"
# Setting up Database for the project
client = MongoClient("mongo")[name]
mongo = MongoDB_wrapper(client)
css_file = "static/styles/index.css"

print("mongoDB is up I think")

# Setting up the Security
security = Security()
print("Security is setup I think")

# Setting up Helper
helper = Helper()
# Setting up the App
app = Flask(name)
print("App running I think")


@app.route("/")  # converts normal function to view function
def homepage():  # view function
    print("Someone is at the homepage", flush=True)

    token = request.cookies.get("token", None)
    helper.Better_Print("token", token)
    token_search = mongo.check_if_user_exist(token)

    if not token_search:
        return render_template("index.html", input="/login", input2="/signup", input4=css_file)
    else:
        user_stat = mongo.grab_user_stat(token)
        return render_template(url_for("display_userhomepage", user_data=user_stat))

# @app.route("/homepage")  # converts normal function to view function
# def home():  # view function
#     print("Someone is at the userpage", flush=True)
#     return render_template("homepage.html", input="username", input2="static/styles/homepage.css",
#                            gamesCount="999", bestCount="123", fruitCount="1234", killCount="220",
#                            leaderboard="/leaderboard",
#                            single="/singlePlayer", lobby="/lobby")


@app.route("/login", methods=["GET"])  # Only get method
def loginPage():
    # alert will be made when password is wrong or change the div box text to have sub text
    # suggestion will be to use cookie to help checking if the login faill 
    # another option will be me senting post request and make it render a differnt valye in the login box when the loginData fail to get datas
    # [Jacky]
    login_status = request.cookies.get("login_status", "Please Login")
    return render_template("login.html", signup_path="/signup", login_post_path="/loginData",
                           css_path="static/styles/login.css", display_message=login_status)
    # return render_template("login.html", input="/loginData") # Files can be served easier with static files check flask documenation


# God I hate python

@app.route("/loginData", methods=["POST", "GET"])
def user_login():
    forumData = request.form
    print(forumData, flush=True)
    username = forumData.get("ret-username", "")
    password = forumData.get("ret-password", "")
    # Checking if the username is recived correctly [# Jacky]
    # print(username, flush=True)

    # Plan
    # 1. Search for the user
    # 2. Check if the user exist in database
    #   2a. If the user exist redirect to /userpage
    #   2b. If the user does not exist redirect back to /login
    # [Jacky]
    searchable_able = {"username": username}
    # Search in the user finish 
    value = mongo.search(searchable_able, "user")
    # Check if the user is in database

    print(value, flush=True)
    print(searchable_able, flush=True)

    if value == None:
        return redirect("/login", code=302)

    value = security.check_password(password, value.get("password", None))

    if not value:
        # If the user does not exist
        # Let redirect user back to /login page
        # TODO: Write data to session cookie
        redirect_respond = redirect("/login", code=302)
        redirect_respond.set_cookie("login_status", "No such user")
        return redirect_respond
    else:
        # If the user name is there
        # redirect datas using cookies
        new_token = security.generate_token(username, request.user_agent)

        hash_token = new_token[0]
        token = new_token[1]

        helper.new_login(mongo, hash_token, username) # This update all the old token in database
        print("new token: " + str(new_token), flush=True)
        search_path = {"authorize_token": hash_token}
        # for i in mongo.database["temp_path"].find():
        #     print("temp_path: ", flush=True)
        #     print(i, flush=True)

        path = mongo.search(search_path, "temp_path").get("path", None)

        #user_datas = mongo.grab_user_stat(token)

        if path == None:
            helper.Better_Print("Path is none", path)
            #helper.Better_Print("Path is none user state value", user_data)
            redirect("/404", code=301)
        respond = redirect(url_for("display_userhomepage", userid=path))

        respond.set_cookie("token", token, 36000)
        return respond


# This is signup
@app.route("/signup", methods=["GET"])  # Only get method
def signup():
    # alert will be made when password is wrong or change the div box text to have sub text
    # suggestion will be to use cookie to help checking if the login faill
    # another option will be me senting post request and make it render a differnt valye in the login box when the loginData fail to get datas
    # [Jacky]
    return render_template("signup.html", signup_post_path="/signupData", login_path="/login",
                           css_path="static/styles/signup.css")
    # return render_template("login.html", input="/loginData") # Files can be served easier with static files check flask documenation


# God I hate python


@app.route("/signupData", methods=["POST"])  # Only post method
def signup_userData():
    forumData = request.form
    print("form data", flush=True)
    print(forumData, flush=True)
    # Can we do a preload of html here or we need to do that in the frontend?

    # Some how get data from the form 
    # Waiting for frontend
    username = forumData.get("new-username", None)
    password = forumData.get("new-password", None)
    # probnley should have a loading screen here maybe

    # this is suppose to clean/ check for bad account and password
    if security.password_and_user_checker(username=username, password=password) or security.duplicate_username(
            username=username, database=mongo):
        # if the input is bad we redirect it to the login page
        return redirect("/sigup", code=302)  # redirect the user to login page after a bad username and password
    else:
        helper.Better_Print("password", password)
        # Let hash the password
        hashed_password = security.hash_and_salt_password(password)

        autho_token = security.generate_token(username, request.user_agent)


        hashed_token = autho_token[0]
        token = autho_token[1]
        # Structure the data input to database
        # Storing the hash of the token
        user = {"username": username, "password": hashed_password, "old_token": hashed_token}
        # Insert the hash password
        mongo.insert(user, "user")

        # Set up the database for user
        path = helper.generate_path()
        temp_path = {"authorize_token": hashed_token, "path": path}
        mongo.insert(temp_path, "temp_path")

        # stored basic user data
        user_authorized_token = {"username": username, "authorize_token": hashed_token}
        mongo.insert(user_authorized_token, "user_authorize_token")

        # user states
        user_states = {"authorize_token": hashed_token, "username": username, "about_me": None, "profile_picture": None,
                       "highest_point": None}
        mongo.insert(user_states, "user_stat")

        # print(format) # User name should be max 12 characters
        # This should be done in the frontend ->
        # special characters that we don't want in username: &, ~, /, <,   >, ;, [space]Hello
        # direct the user to the user homepage [#Jacky]
        return redirect("/login", code=302)


@app.route("/leaderboard", methods=["GET"])
def display_leaderBoard():
    return render_template("leaderboard.html", style="static/styles/leaderboard.css")


@app.route("/rank", methods=["GET"])
def ranked_users():
    rank = [{"username": "a", "highest_point": 123}, {"username": "c", "highest_point": 121},
            {"username": "b", "highest_point": 122}]

    # scores = mongo.database["user_stat"]
    # rank = scores.find({},{"authorize_token": 0, "username": 1, "about_me": 0, "profile_picture": 0, "highest_point": 1})
    def sortkey(score):
        return score["highest_point"]

    rank = sorted(rank, key=sortkey, reverse=True)
    return rank


# Not needed
# @app.route("/changelog", methods=["POST", "GET"])
# def display_changelog():
#     change_data = open("changelogs.txt", "r").readlines()
#
#     # Change the change log into three selection so I can display them better
#
#     # This will use the template feature of flask and use that to display a text file that I will write on the side for all the changes I made and the goals this can also be used to test
#     return render_template("changelog.html", change=change_data)
@app.route("/userpage/<userid>")
def display_userhomepage(userid):
    # display the userhomepage
    # Using render_template I can use the same html for all user to make them feel special
    # Grab usernameq
    # Change later for the actual html

    # Checks if the auth token actual matches with the path
    token = request.cookies.get("token", None)

    if token == None:
        return redirect("/404")


    # Checks if the author token matches with the path
    result_path = mongo.check_if_path_exist(userid, token) # check if the path exist

    if result_path == None:
        return redirect("/404")
    else:
        user_data = mongo.grab_user_stat(token)
        return render_template("homepage.html",
                               css_file="../static/styles/homepage.css",
                               leaderboard="/leaderboard",
                               single="/singlePlayer",
                               lobby="/lobby",
                               join_lobby="/join_lobby",
                               user_username=user_data["username"],
                               user_highscore=user_data["highest_point"],
                               user_aboutme=user_data["about_me"],
                               user_profile_picture=user_data["profile_picture"]
                               )


app.run()  # Don't use this for final product [#Jacky]
