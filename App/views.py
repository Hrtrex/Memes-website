from flask import Flask, redirect, url_for, render_template
from App import app
from App.db import get_db_connection

@app.route("/")
def home():
    return "<h1>Home page</h1>"

@app.route("/<name>")
def user(name):
    conn = get_db_connection()
    temps = conn.execute('SELECT * from blokady').fetchall()
    conn.close()
    return render_template("index.html", name=name, sqls=temps)

@app.route("/admin")
def admin():
    return redirect(url_for("home"))

@app.route("/jbzd/<page>")
def jbzd():
    return render_template("index.html")