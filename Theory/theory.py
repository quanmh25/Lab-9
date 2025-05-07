import flask as fl 
from flask import redirect, url_for, render_template, request, session, flash

import datetime as dt



app = fl.Flask(__name__, template_folder="Theory/templates")

app.config["SECRET_KEY"] = "mothighbar"
app.permanent_session_lifetime = dt.timedelta(minutes=1)

@app.route('/')
def index():
    return redirect(url_for('hello'))  # hoặc return render_template('home.html')

@app.route('/home')
def hello():
    return render_template('home.html')

@app.route("/login", methods=["GET", "POST"])
def login():
    if fl.request.method == "POST":
        name = fl.request.form.get("name")
        session.permanent = True
        flash("You logged in sucessfully!", "info")
        return render_template("home.html")
    return render_template("login.html")

@app.route("/user")
def helloUser():
    if "user" in session:
        name = session["user"]
        return f"<h1> Hello {name} </h1>"
    else:
        return redirect(url_for("login"))

@app.route("/logout")
def logout():
    flash("You have already logged out!", "info")
    session.pop("user", None)
    return redirect(url_for("login"))



if __name__ == '__main__':
    app.run(debug=True)