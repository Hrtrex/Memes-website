from flask import Flask, redirect, url_for, render_template
from App import app
import psycopg2
from App.memes import get_urls_jbzd, get_urls_kwejk

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

@app.route("/komentarze")
def komentarze():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('select * from memy;')
    memy = cur.fetchall()
    cur.execute('select * from komentarze where komentarze_id_komentarza is null;')
    komentarze=cur.fetchall()
    cur.execute('select * from komentarze where komentarze_id_komentarza is not null')
    odpowiedzi=cur.fetchall()
    cur.execute('select komentarze.id_komentarza,(dodatnie.plusy) as fajny, (ujemne.minusy) as nieladny from komentarze, (select komentarze_id_komentarza,sum(jaka_ocena) as plusy from oceny_komentarzy group by komentarze_id_komentarza) as dodatnie, (select komentarze_id_komentarza,count(jaka_ocena) as minusy from oceny_komentarzy where jaka_ocena=0 group by komentarze_id_komentarza) as ujemne where komentarze.id_komentarza=dodatnie.komentarze_id_komentarza and komentarze.id_komentarza = ujemne.komentarze_id_komentarza;')
    oceny=cur.fetchall()
    cur.execute('select komentarze_id_komentarza, count(komentarze_id_komentarza) as ilosc from komentarze where komentarze_id_komentarza is not null group by komentarze_id_komentarza;')
    ileodp=cur.fetchall()
    cur.close()
    conn.close()
    return render_template('komentarz.html', memy=memy,komentarze=komentarze,odpowiedzi=odpowiedzi,oceny=oceny,ileodp=ileodp)


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

