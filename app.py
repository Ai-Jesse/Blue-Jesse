from flask import Flask

print("App running I think")

app = Flask("blue_Jesse")

@app.route("/")
def homepage():
    print("I'm here")
    return "<h1>Welcome!</h1>"


# app.run() # Don't use this for final product [#Jacky]