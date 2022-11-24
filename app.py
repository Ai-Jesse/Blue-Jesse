from API import MongoDB_wrapper
from flask import Flask, render_template, request
from pymongo import MongoClient


# Setting up Database for the project
client = MongoClient("mongo")
mongo = MongoDB_wrapper(client)
css_file = "static/style.css"

print("mongoDB is up I think")
app = Flask("blue_Jesse")
print("App running I think")


@app.route("/") # converts normal function to view function
def homepage(): # view function
    print("Someone is at the homepage", flush=True)
    return render_template("index.html", input="/login", input2="/signup", input3="/homepage", input4=css_file)

@app.route("/homepage") # converts normal function to view function
def home(): # view function
    print("Someone is at the userpage", flush=True)
    return render_template("homepage.html", input="/homepage")

@app.route("/signup") # converts normal function to view function
def login(): # view function
    print("Someone is at the homepage", flush=True)
    return render_template("signup.html", input="/login", input2="/signUpData")
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
    return render_template("login.html", input="/signup", input2="/loginData") # Files can be served easier with static files check flask documenation


@app.route("/loginData", methods=["POST"]) # Only post method
def logging_userData():
    r=request.form # User name should be max 12 characters
    print(r)
    # special characters that we don't want in username: &, ~, /, <, >, ;, [space]
    
@app.route("/signUpData", methods=["POST"]) # Only post method
def signingup_userData():
    print(request) # User name should be max 12 characters
    # special characters that we don't want in username: &, ~, /, <, >, ;, [space]
 



# app.run() # Don't use this for final product [#Jacky]

