from flask import Flask, redirect, url_for, render_template
from App import app
from App.memes import get_urls_jbzd, get_urls_kwejk

@app.route("/")
def home():
    return "<h1>Home page</h1>"

@app.route("/<name>")
def user(name):
    return render_template("index.html", name=name)

@app.route("/admin")
def admin():
    return redirect(url_for("home"))

@app.route("/jbzd/", defaults={'page': ''})
@app.route("/jbzd/<page>")
def jbzd(page):
    urls, votes = get_urls_jbzd(page)
    data = list(zip(urls, votes))
    return render_template("index.html", test=data)

@app.route("/kwejk/", defaults={'page': ''})
@app.route("/kwejk/<page>")
def kwejk(page):
    urls, votes = get_urls_kwejk(page)
    data = list(zip(urls, votes))
    return render_template("index.html", test=data)
