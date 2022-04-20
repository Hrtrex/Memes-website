from flask import Flask, redirect, url_for, render_template
from App import app


@app.route("/")
def home():
    return "<h1>Home page</h1>"

@app.route("/<name>")
def user(name):
    return render_template("index.html", content=name)

@app.route("/admin")
def admin():
    return redirect(url_for("home"))

@app.route("/jbzd/<page>")
def jbzd():
    return render_template("index.html")