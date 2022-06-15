from flask import Flask, redirect, url_for, render_template, request, flash, session
from App import app
import psycopg2
import psycopg2.extras
import re
import werkzeug
from werkzeug.security import generate_password_hash, check_password_hash
from App.memes import get_urls_jbzd, get_urls_kwejk
from datetime import date, datetime
import random
import os
from argparse import Namespace




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

@app.route("/jbzd/", defaults={'page': ''})
@app.route("/jbzd/<page>")
def jbzd(page):
    urls, votes = get_urls_jbzd(page)
    data = list(zip(urls, votes))
    return render_template("memy.html", links=data)

@app.route("/kwejk/", defaults={'page': ''})
@app.route("/kwejk/<page>")
def kwejk(page):
    urls, votes = get_urls_kwejk(page)
    data = list(zip(urls, votes))
    return render_template("memy.html", links=data)


#LOGOWANIE
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != '12345':
            error = 'Invalid Credentials. Please try again.'
        else:
            return redirect(url_for('home'))
    return render_template('login.html', error=error)




#REJESTRACJA
@app.route('/register', methods = ['POST', 'GET'])
def register():
    return render_template('register.html')


@app.route('/userPanel', methods = ['POST', 'GET'])
def userP():
   
    password = 0
    password2 = 0
    email = 0
    if request.method == 'GET':
        return f"FATAL ERROR"
    if request.method == 'POST':
        register_data = request.form
        n = Namespace(**register_data)
        user_role_test = 0
        if n.login == 'admin':
            user_role_test = 2
        else:
            user_role_test = 1

    
        if n.password != n.password2:
            return 'Wrong password confirmation', 400

        

        join = date.today()
        hashed_password = generate_password_hash(n.password)

        login = n.login
        password = hashed_password
        email = n.email
        user_role = user_role_test
        joined = join
        
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('select * from uzytkownicy')
        cur.execute("""
        INSERT INTO uzytkownicy (login, haslo, email, typ_uzytkownika, data_dolaczenia)
        VALUES (%s, %s, %s, %s, %s);
        """,
        (login, password, email, user_role, joined))
        
        conn.commit()
        cur.close()
        conn.close()

        return render_template('userPanel.html',register_data = register_data, n=n, user_role = user_role, joined=joined)



#reset hasla
@app.route('/passwordReset')
def resetP():
    return render_template('passwordReset.html')




#email ver.
@app.route('/emailCheck')
def emailcheck():
    return render_template('emailCheck.html')

