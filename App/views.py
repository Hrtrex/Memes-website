from flask import Flask, redirect, url_for, render_template
from App import app
from App.db import get_db_connection
import psycopg2

def get_db_connection():
    conn = psycopg2.connect(host='flask-server.postgres.database.azure.com',
                            database='db',
                            user='hrtrex',
                            password='Jebacdisa_12',
                            sslmode='require')
    return conn

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/memesRanking")
def getMemesSortedByRatings():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('select id_mema,tytul,kategoria,CAST(avg(jaka_ocena) as NUMERIC(10,1)) srednia from oceny_memow,memy where memy.id_mema=oceny_memow.Memy_id_mema group by id_mema having avg(jaka_ocena) is not null order by srednia desc;')
    memy = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('memesRanking.html', memy=memy)

@app.route("/<name>")
def user(name):
    return render_template("index.html")

@app.route("/admin")
def admin():
    return redirect(url_for("home"))

@app.route("/jbzd/<page>")
def jbzd():
    return render_template("index.html")