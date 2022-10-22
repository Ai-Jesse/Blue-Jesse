from flask import Flask, render_template

print("App running I think")

app = Flask("blue_Jesse")

@app.route("/") # converts normal function to view function
def homepage(): # view function
    print("Someone is at the homepage")
    return render_template("index.html")

    '''
    When calling render_templates it search for the html files in the template folder
    you can pass in a key value pair to override the value at the localtion of the html template example:
    ----html----
    e.g. {{test}}
    ----html----
    render_template(html, test=5) [#Jacky]
    '''

@app.route("/login")
def loginPage():
    return render_template("login.html") # Files can be served easier with static files check flask documenation








# app.run() # Don't use this for final product [#Jacky]

