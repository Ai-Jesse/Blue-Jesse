# from urllib import request
import code
from API import MongoDB_wrapper, Security, Helper
from game import *
from flask import Flask, render_template, redirect, request, url_for, session, make_response
from pymongo import MongoClient
import json
from flask_sock import Sock
import threading

# Just added gpg to my second laptop let see if this works[#Jacky]


# Web Application name: blue_Jesse
name = "blue_Jesse"
# Setting up Database for the project
client = MongoClient("mongo")[name]
mongo = MongoDB_wrapper(client)
css_file = "static/styles/index.css"

# print("mongoDB is up I think")

# Setting up the Security
security = Security()
# print("Security is setup I think")

# Setting up Helper
helper = Helper()
# Setting up the App
app = Flask(name)
# print("App running I think")
sock = Sock(app)

@app.after_request # add nosniff to all response
def add_nosniff(response):
    response.headers["X-Content-Type-Options"] = "nosniff"
    return response

@app.route("/")  # converts normal function to view function
def homepage():  # view function
    # print("Someone is at the homepage", flush=True)

    token = request.cookies.get("token", None)
    # helper.Better_Print("token", token)
    token_search = mongo.check_if_user_exist(token)

    if not token_search:
        return render_template("index.html", input="/login", input2="/signup", input4=css_file)
    else:
        path = mongo.grab_path(token)
        # helper.Better_Print("path at homepage", path)
        return redirect(url_for("display_userhomepage", userid=path))

# @app.route("/homepage")  # converts normal function to view function
# def home():  # view function
#     print("Someone is at the userpage", flush=True)
#     return render_template("user_Private_Homepage.html", input="username", input2="static/styles/homepage.css",
#                            gamesCount="999", bestCount="123", fruitCount="1234", killCount="220",
#                            leaderboard="/leaderboard",
#                            single="/singlePlayer", lobby="/lobby")


@app.route("/login", methods=["GET"])  # Only get method
def loginPage():
    # alert will be made when password is wrong or change the div box text to have sub text
    # suggestion will be to use cookie to help checking if the login faill 
    # another option will be me senting post request and make it render a differnt valye in the login box when the loginData fail to get datas
    # [Jacky]
    xsrf = helper.generate_xsrf_token(mongo, "login_xsrf")
    login_status = request.cookies.get("login_status", "Please Login")
    return render_template("login.html", signup_path="/signup", login_post_path="/loginData",
                           css_path="static/styles/login.css", display_message=login_status, xsrf=xsrf)
    # return render_template("login.html", input="/loginData") # Files can be served easier with static files check flask documenation


# God I hate python

@app.route("/loginData", methods=["POST", "GET"])
def user_login():
    forumData = request.form
    xsrf = forumData.get("login-xsrf")
    if not helper.check_xsrf_token(xsrf, mongo, "login_xsrf"):
        return redirect("/login")
    # print(forumData, flush=True)
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

    # print(value, flush=True)
    # print(searchable_able, flush=True)

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
        # print("new token: " + str(new_token), flush=True)
        search_path = {"authorize_token": hash_token}
        # for i in mongo.database["temp_path"].find():
        #     print("temp_path: ", flush=True)
        #     print(i, flush=True)

        path = mongo.search(search_path, "temp_path").get("path", None)

        #user_datas = mongo.grab_user_stat(token)

        if path == None:
            # helper.Better_Print("Path is none", path)
            #helper.Better_Print("Path is none user state value", user_data)
            redirect("/404", code=301)

        # helper.Better_Print("Find Path", path)
        respond = redirect(url_for("display_userhomepage", userid=path))

        respond.set_cookie("token", token, 36000, httponly=True)
        return respond


# This is signup
@app.route("/signup", methods=["GET"])  # Only get method
def signup():
    # alert will be made when password is wrong or change the div box text to have sub text
    # suggestion will be to use cookie to help checking if the login faill
    # another option will be me senting post request and make it render a differnt valye in the login box when the loginData fail to get datas
    # [Jacky]
    xsrf = helper.generate_xsrf_token(mongo, "signup_xsrf")
    return render_template("signup.html", signup_post_path="/signupData", login_path="/login",
                           css_path="static/styles/signup.css", xsrf=xsrf)
    # return render_template("login.html", input="/loginData") # Files can be served easier with static files check flask documenation


# God I hate python


@app.route("/signupData", methods=["POST"])  # Only post method
def signup_userData():
    forumData = request.form
    xsrf = forumData.get("signup-xsrf")
    if not helper.check_xsrf_token(xsrf, mongo, "signup_xsrf"):
        return redirect("/signup")
    # print("form data", flush=True)
    # print(forumData, flush=True)
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
        return redirect("/signup", code=302)  # redirect the user to login page after a bad username and password
    else:
        # helper.Better_Print("password", password)
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
        temp_path = {"authorize_token": hashed_token, "path": path, "profile_status": "private"}
        mongo.insert(temp_path, "temp_path")

        # stored basic user data
        user_authorized_token = {"username": username, "authorize_token": hashed_token}
        mongo.insert(user_authorized_token, "user_authorize_token")

        # user states
        user_states = {"authorize_token": hashed_token, "username": username, "about_me": None, "profile_picture": None,
                       "highest_point": None, "profile_status": "private"}
        mongo.insert(user_states, "user_stat")

        # print(format) # User name should be max 12 characters
        # This should be done in the frontend ->
        # special characters that we don't want in username: &, ~, /, <,   >, ;, [space]Hello
        # direct the user to the user homepage [#Jacky]
        return redirect("/login", code=302)


@app.route("/leaderboard", methods=["GET"])
def display_leaderBoard():
    query_dict = {"profile_status": "public"}
    list_user = mongo.grab_all_user_stat(query_dict)
    user_ranking_data = []
    for user in list_user:
        # overrivewing some dumb changes
        # only works with public profiles create 10 user for test
        user_ranking = {}
        user_ranking["name"] = user["username"]
        user_ranking["highest_point"] = user["highest_point"]
        user_ranking_data.append(user_ranking)

    user_ranking_data.sort(reverse=True, key=helper.leadboard_ranking_sort)

    for i in range(len(user_ranking_data)):
        user_ranking_data[i]["rank"] = i + 1

    # helper.Better_Print("user ranking at leaderbord", user_ranking_data)
    return render_template("leaderboard.html", style="static/styles/leaderboard.css", user_stat=user_ranking_data, input="/userpage")


# @app.route("/rank", methods=["GET"])
# def ranked_users():
#     rank = [{"username": "a", "highest_point": 123}, {"username": "c", "highest_point": 121},
#             {"username": "b", "highest_point": 122}]
#
#     # scores = mongo.database["user_stat"]
#     # rank = scores.find({},{"authorize_token": 0, "username": 1, "about_me": 0, "profile_picture": 0, "highest_point": 1})
#     def sortkey(score):
#         return score["highest_point"]
#
#     rank = sorted(rank, key=sortkey, reverse=True)
#     return rank
#

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
    # helper.Better_Print("token at userpage", token)
    if token == None:
        return redirect("/404")


    # Checks if the author token matches with the path
    result_path = mongo.check_if_path_exist(userid, token) # check if the path exist
    # helper.Better_Print("result path", result_path)
    # Check if the profile is public
    # result_public = mongo.vist_public_profile(userid, token)
    # helper.Better_Print("result public", result_public)



    if result_path == None:
        return redirect("/404")
    elif result_path != None:
        # if the user is the owner of the page
        join_lobby_xsrf = helper.generate_xsrf_token(mongo, "game_room_xsrf", token)
        change_profile_xsrf = helper.generate_xsrf_token(mongo, "change_profile_xsrf", token)
        logout_xsrf = helper.generate_xsrf_token(mongo, "logout_xsrf", token)

        # helper.Better_Print("Owner of the page is here", result_path)
        user_data = mongo.grab_user_stat(token)
        # helper.Better_Print("profile status", user_data.get("profile_status", "does not exist"))
        return render_template("user_Private_Homepage.html",
                               css_file="../static/styles/homepage.css",
                               leaderboard="/leaderboard",
                               single="/singleplayer",
                               lobby="/lobby/new",
                               join_lobby="/lobby/join",
                               user_username=user_data.get("username", None),
                               user_highscore=user_data.get("highest_point", None),
                               user_aboutme=user_data.get("about_me", None),
                               user_profile_status=user_data.get("profile_status", None),
                               user_profile_picture=user_data.get("profile_picture", None),
                               join_lobby_xsrf=join_lobby_xsrf,
                               change_profile_xsrf=change_profile_xsrf,
                               logout_xsrf=logout_xsrf
                               )
    else:
        return redirect("/404")

# @app.route("userpage/<userid>/<setting>")
# def display_setting():
#     return

@app.route("/404")
def display_error():
    return render_template("404.html")

@app.route("/userpage")
def redirect_to_correct():
    token = request.cookies.get("token", None)
    token_checker = mongo.check_if_token_exist(token)
    # print("token checker: " + str(token_checker), flush=True)
    if token_checker == None:
        return redirect("/")
    else:
        path = mongo.grab_path(token)
        # helper.Better_Print("path at userpage/ only", path)
        return redirect(url_for("display_userhomepage", userid=path))
@app.route("/userpage/change_profile", methods=["POST"])
def change_profile_status():
    token = request.cookies.get("token", None)
    token_checker = mongo.check_if_token_exist(token)
    # print("token checker: " + str(token_checker), flush=True)
    if token_checker == None:
        return redirect("/")
    else:
        xsrf = request.form.get("change_profile-xsrf")
        if not helper.check_xsrf_token(xsrf, mongo, "change_profile_xsrf", token):
            return redirect("/")
        value = ""
        actual_value =token_checker.get("profile_status", None)
        # print("actual value: " + str(actual_value), flush=True)
        if actual_value == "private":
            value = value + "public"
        elif actual_value == None:
            redirect("/", code=302)
        else:
            value = value + "private"
        update_value = {"profile_status": value}
        mongo.update(token_checker, update_value, "user_stat")
    path = mongo.grab_path(token)
    respond = redirect(url_for("display_userhomepage", userid=path))
    return respond

@app.route("/singleplayer")
def singleplayer():
    token = request.cookies.get("token", None)
    token_checker = mongo.check_if_token_exist(token)
    if token_checker == None:
        return redirect("/userpage")

    return render_template("singlegame.html")

#establish singleplayer websocket connection
@sock.route("/singleplayer") 
def ws_singleplayer(ws):

    token = request.cookies.get("token", None)
    token_checker = mongo.check_if_token_exist(token)
    if token_checker == None:
        return 

    #create a singleplayer game, will keep recieving data and pass it to the game object, handle the code in game class
    game = SingleGame(ws, token=token)

    while True:
        try:
            data = ws.receive()
            game.handle(data)
        except:
            try:
                ws.close()
            except:
                pass
            del game
            break

@app.route("/lobby/<path>", methods=["GET", "POST"])
def lobby(path):
    token = request.cookies.get("token", None)
    token_checker = mongo.check_if_token_exist(token)
    if token_checker == None:
        return redirect("/userpage")

    if not path:
        return redirect("/userpage")

    if path == "new" and request.method == "GET":
        room = Lobby()
        code = room.code
        return redirect("/lobby/" + code, code = 302)
    elif path == "join" and request.method == "POST":
        form = request.form
        code = form.get("code")
        xsrf_token = form.get("join_lobby-xsrf")
        if helper.check_xsrf_token(xsrf_token, mongo, "game_room_xsrf", token) and code:
            return redirect("/lobby/" + code, code = 302)
    else:
        if Lobby.lobbies.get(path, False):
            if len(Lobby.lobbies.get(path).socket) < 2:
                for i in Lobby.lobbies.get(path, False).socket:
                    if i["token"] == token:
                        return redirect("/userpage", code=302)
                xsrf_token = helper.generate_xsrf_token(mongo, "chat_xsrf", token)
                return render_template("lobby.html", room_code=path, xsrf_token=xsrf_token, input4="/static/styles/lobby.css")
    return redirect("/userpage", code=302)
        

@sock.route("/lobby/<path>")
def ws_host_room(ws, path):
    token = request.cookies.get("token", None)
    token_checker = mongo.check_if_token_exist(token)
    if token_checker == None:
        return 
    
    room = Lobby.lobbies.get(path, False)
    
    if room and len(room.socket) < 2:
        for i in room.socket:
            if i["token"] == token:
                return
    else:
        return
    
    room.join(ws, token)
    
    while True:
        try:
            data = ws.receive()
            room.handle(data, ws)
        except:
            try:
                room.leave(ws)
            except:
                break

@app.route("/multigame/<path>")
def multi_game(path):
    token = request.cookies.get("token", None)
    token_checker = mongo.check_if_token_exist(token)
    if token_checker == None:
        return redirect("/userpage")

    game = MultiGame.games.get(path, False)
    if game and not MultiGame.games.get(path).game_start:
        if game.player1.token == token or game.player2.token == token:
            return redirect("/userpage", code=302)
        return render_template("multigame.html")
    return redirect("/userpage", code=302)

@sock.route("/multigame/<path>")
def ws_multi_game(ws, path):
    token = request.cookies.get("token", None)
    token_checker = mongo.check_if_token_exist(token)
    if token_checker == None:
        return redirect("/userpage")

    game = MultiGame.games.get(path, False)
    
    if game and not game.game_start:
        if game.player1.token == token or game.player2.token == token:
            return
    else:
        return
    
    game.join(ws, token)

    while True:
        try:
            data = ws.receive()
            game.handle(data, ws)
        except:
            try:
                game.leave(ws)
            except:
                break

@app.route("/userpage/logout", methods=["POST"])
def logout():
    token = request.cookies.get("token", None)
    token_checker = mongo.check_if_token_exist(token)
    if token_checker == None:
        return redirect("/userpage")

    xsrf_token = request.form.get("logout-xsrf")
    if not helper.check_xsrf_token(xsrf_token, mongo, "logout_xsrf", token):
        return redirect("/userpage")
    

    respond =  redirect("/", code=302)
    respond.delete_cookie("token")
    respond.delete_cookie("login_status")
    return respond

@app.errorhandler(404)
def go_back_to_home(error):
    return redirect("/")


@app.errorhandler(500)
def go_back(error):
    return redirect("/")

# app.run()  # Don't use this for final product [#Jacky]
