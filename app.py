
# from urllib import request
import code
from API import MongoDB_wrapper, Security
from flask import Flask, render_template, redirect, request, url_for, session
from pymongo import MongoClient
import json

# Just added gpg to my second laptop let see if this works[#Jacky]


# Web Application name: blue_Jesse
name = "blue_Jesse"
# Setting up Database for the project
client = MongoClient("mongo")[name]
mongo = MongoDB_wrapper(client)
css_file = "static/style.css"

print("mongoDB is up I think")

# Setting up the Security
security = Security()
print("Security is setup I think")

# Setting up the App
app = Flask(name)
print("App running I think")


@app.route("/") # converts normal function to view function
def homepage(): # view function
    print("Someone is at the homepage", flush=True)
    return render_template("index.html", input="/login", input2="/signup", input3="/homepage", input4=css_file)

@app.route("/homepage") # converts normal function to view function
def home(): # view function
    print("Someone is at the userpage", flush=True)
    return render_template("homepage.html", input="/homepage")

@app.route("/login", methods=["GET"]) # Only get method
def loginPage():
    # alert will be made when password is wrong or change the div box text to have sub text
    # suggestion will be to use cookie to help checking if the login faill 
    # another option will be me senting post request and make it render a differnt valye in the login box when the loginData fail to get datas
    # [Jacky]
    login_status = request.cookies.get("login_status", "Please Login")
    return render_template("login.html", signup_path="/signup", login_post_path="/loginData", css_path="", display_message=login_status)
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
    password = security.hash_265(password)
    searchable_able = {"username" : username, "password": password}
    # Search in the user finish 
    value = mongo.search(searchable_able, "user")
    # Check if the user is in database

    print(value, flush=True)
    print(searchable_able, flush=True)
    if value == None:
        # If the user does not exist
        # Let redirect user back to /login page
        # TODO: Write data to session cookie

        redirect_respond = redirect("/login", code=302)
        redirect_respond.set_cookie("login_status", "No such user")
        return redirect_respond
    elif value["password"] != searchable_able["password"]:
        # TODO: Write data to session cookie about wrong password
        redirect_respond = redirect("/login", code=302)
        redirect_respond.set_cookie("log_status", "Wrong password")
        return redirect_respond
    else:
    # If the user name is there
        # redirect datas using cookies
        return redirect(url_for("display_userhomepage", userid="Hello"))

# This is signup
@app.route("/signup", methods=["GET"]) # Only get method
def signup():
    # alert will be made when password is wrong or change the div box text to have sub text
    # suggestion will be to use cookie to help checking if the login faill
    # another option will be me senting post request and make it render a differnt valye in the login box when the loginData fail to get datas
    # [Jacky]
    return render_template("signup.html", signup_post_path="/signupData", login_path="/login")
    # return render_template("login.html", input="/loginData") # Files can be served easier with static files check flask documenation
# God I hate python


@app.route("/signupData", methods=["POST"]) # Only post method
def signup_userData():
    forumData = request.form
    print("form data", flush=True)
    print(forumData, flush=True)
    # Can we do a preload of html here or we need to do that in the frontend?
    
    # Some how get data from the form 
    # Waiting for frontend
    username = forumData.get("new-username")
    password = forumData.get("new-password")
    # probnley should have a loading screen here maybe
    
    # this is suppose to clean/ check for bad account and password
    if security.password_and_user_checker(username=username, password=password):
        # if the input is bad we redirect it to the login page
        return redirect("/login", code=302) # redirect the user to login page after a bad username and password
    else:    
        # Let hash the password
        hashed_password = security.hash_265(password)
        # Structure the data input to database
        user = {"username": username, "password": hashed_password}
        # Insert the hash password
        mongo.insert(user, "user")
        # print(format) # User name should be max 12 characters
        # This should be done in the frontend ->
        # special characters that we don't want in username: &, ~, /, <,   >, ;, [space]Hello
        # direct the user to the user homepage [#Jacky]
        return redirect("/login", code=302)

@app.route("/changelog", methods=["POST", "GET"])
def display_changelog():
    change_data = open("changelogs.txt", "r").readlines()


    # Change the change log into three selection so I can display them better
    
    # This will use the template feature of flask and use that to display a text file that I will write on the side for all the changes I made and the goals this can also be used to test
    return render_template("changelog.html", change=change_data)

@app.route("/userpage/<userid>")
def display_userhomepage(userid):
    # display the userhomepage
    # Using render_template I can use the same html for all user to make them feel special
    # Grab username
    # Change later for the actual html
    return render_template("QuickTest.html", value=userid)
# app.run() # Don't use this for final product [#Jacky]