from flask import Flask, render_template

print("App running I think")

app = Flask("blue_Jesse")

@app.route("/")
def homepage():
    print("Someone is at the homepage")
    return render_template("data/index.html")

@app.route("/login")
def loginPage():
    return render_template("data/login.html") # Files can be served easier with static files check flask documenation








# app.run() # Don't use this for final product [#Jacky]

