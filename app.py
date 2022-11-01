# from urllib import request
import code
from API import MongoDB_wrapper, Security
from flask import Flask, render_template, redirect, request, url_for
from pymongo import MongoClient

import json


# Just added gpg to my second laptop let see if this works[#Jacky]


# Web Application name: blue_Jesse
name = "blue_Jesse"
# Setting up Database for the project
client = MongoClient("mongo")[name]
mongo = MongoDB_wrapper(client)
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
    return render_template("index.html", input="/login")
    '''
    When calling render_templates it search for the html files in the template folder
    you can pass in a key value pair to override the value at the localtion of the html template example:
    ----html----
    e.g. {{test}}
    ----html----
    render_template(html, test=5) [#Jacky]
    '''
@app.route("/login", methods=["GET"]) # Only get method
def loginPage():
    return render_template("login.html", input="/loginData", script="") # Files can be served easier with static files check flask documenation

    # alert will be made when password is wrong or change the div box text to have sub text
# God I hate python

@app.route("/loginData", methods=["POST", "GET"])
def user_login():
    forumData = request.form

    username = forumData["username"]
    password = forumData["password"]

    # Checking if the username is recived correctly [# Jacky]
    # print(username, flush=True)

    # Plan
    # 1. Search for the user
    # 2. Check if the user exist in database
    #   2a. If the user exist redirect to /userpage
    #   2b. If the user does not exist redirect back to /login
    # [Jacky]

    searchable_able = {"username" : username, "password": password}
    # test
    # Search in the user finish 
    value = mongo.search(searchable_able, "user")

    # Check if the user is in database
    if value == None:
        # If the user does not exist
        # Let redirect user back to /login page
        return redirect("/login")
    else:

        
        return 0

# This is signup data I mess up
@app.route("/singupData", methods=["POST"]) # Only post method
def logging_userData():
    forumData = request.form
    # Can we do a preload of html here or we need to do that in the frontend?
    
    # Some how get data from the form 
    # Waiting for frontend
    username = ""
    password = ""
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
        MongoDB_wrapper.insert(user)
        # print(format) # User name should be max 12 characters
        # special characters that we don't want in username: &, ~, /, <,   >, ;, [space]
        # direct the user to the user homepage [#Jacky]

@app.route("/changelog", methods=["POST", "GET"])
def display_changelog():
    change_data = open("changelogs.txt", "r").readlines()


    # Change the change log into three selection so I can display them better
    
    # This will use the template feature of flask and use that to display a text file that I will write on the side for all the changes I made and the goals this can also be used to test
    return render_template("changelog.html", change=change_data)

@app.route("/userpage")
def display_userhomepage():
    # display the userhomepage

    # Using render_template I can use the same html for all user to make them feel special

    # Grab username

    return
# app.run() # Don't use this for final product [#Jacky]