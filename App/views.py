from flask import Flask, redirect, url_for, render_template, request
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
def getZgloszenia():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('select id_zgloszenia,zgloszenia_komentarzy.tresc as powod,komentarze.tresc as komentarz,czy_rozpatrzony,zgloszenia_komentarzy.komentarze_id_komentarza,zgloszenia_komentarzy.uzytkownicy_id_uzytkownika as zglaszajacyid,zgl.login as zglaszajacy,data_dodania,komentarze.uzytkownicy_id_uzytkownika as komentujacyid,kom.login as komentujacy from zgloszenia_komentarzy, komentarze,(select id_uzytkownika, login from uzytkownicy) zgl,(select id_uzytkownika,login from uzytkownicy) kom where czy_rozpatrzony=false and zgloszenia_komentarzy.uzytkownicy_id_uzytkownika = zgl.id_uzytkownika and  komentarze.uzytkownicy_id_uzytkownika = kom.id_uzytkownika and zgloszenia_komentarzy.komentarze_id_komentarza = komentarze.id_komentarza order by data_dodania desc;')
    zgloszeniakom = cur.fetchall()
    cur.execute('select id_zgloszenia,zgloszenia_memow.tresc as powod,memy.nazwa_pliku as obraz,czy_rozpatrzony,zgloszenia_memow.memy_id_mema,zgloszenia_memow.uzytkownicy_id_uzytkownika as zglaszajacyid,zgl.login as zglaszajacy,data_dodania,memy.uzytkownicy_id_uzytkownika as wstawiajacyid,wst.login as wstawiajacy from zgloszenia_memow,memy,(select id_uzytkownika, login from uzytkownicy) zgl,(select id_uzytkownika,login from uzytkownicy) wst where czy_rozpatrzony=false and zgloszenia_memow.memy_id_mema = memy.id_mema and zgloszenia_memow.uzytkownicy_id_uzytkownika = zgl.id_uzytkownika and  memy.uzytkownicy_id_uzytkownika = wst.id_uzytkownika order by data_dodania desc;')
    zgloszeniamem = cur.fetchall()
    id_zgl_kom = [x[0] for x in zgloszeniakom]
    id_zgl_mem = [x[0] for x in zgloszeniamem]
    n_zgl_kom = len(id_zgl_kom)
    n_zgl_mem = len(id_zgl_mem)
    cur.close()
    conn.close()
    return render_template("admin.html", zgloszeniamem = zgloszeniamem, zgloszeniakom = zgloszeniakom, id_zgl_kom = id_zgl_kom, id_zgl_mem = id_zgl_mem, n_zgl_kom = n_zgl_kom, n_zgl_mem = n_zgl_mem)

@app.route("/adminActionMem", methods=['POST'])
def adminActionMem():
    action_request = request.form["action"]
    for i in range(len(action_request)):
        if action_request[i].isdigit() == True:
            action = action_request[:i]
            id = action_request[i:]
            break
    conn = get_db_connection()
    cur = conn.cursor()
    if action=="zamknij":
        cur.execute("update zgloszenia_memow set czy_rozpatrzony = true where id_zgloszenia = "+id+";")
        conn.commit()
    if action=="usun":
        cur.execute("update zgloszenia_memow set czy_rozpatrzony = true where memy_id_mema in (select memy_id_mema from zgloszenia_memow where id_zgloszenia ="+id+");")
        conn.commit()
        cur.execute("delete from memy where id_mema = (select memy_id_mema from zgloszenia_memow where id_zgloszenia ="+id+");")
        conn.commit()
    if action=="ban":
        ban_duration = request.form["banDuration"];
        ban_reason ="'"+request.form["banReason"]+"'"
        ban_enddate = "CURRENT_DATE"+" + "+ban_duration
        cur.execute("update zgloszenia_memow set czy_rozpatrzony = true where id_zgloszenia = "+id+";")
        conn.commit()
        cur.execute("insert into blokady values (default,CURRENT_DATE,"+ban_enddate+","+ban_reason+","+id+");")
        conn.commit()
    cur.close()
    conn.close()
    return redirect("/admin")

@app.route("/adminActionKom", methods=['POST'])
def adminActionKom():
    action_request = request.form["action"]
    for i in range(len(action_request)):
        if action_request[i].isdigit() == True:
            action = action_request[:i]
            id = action_request[i:]
            break
    conn = get_db_connection()
    cur = conn.cursor()
    if action=="zamknij":
        cur.execute("update zgloszenia_komentarzy set czy_rozpatrzony = true where id_zgloszenia = "+id+";")
        conn.commit()
    if action=="usun":
        cur.execute("update zgloszenia_komentarzy set czy_rozpatrzony = true where komentarze_id_komentarza in (select komentarze_id_komentarza from zgloszenia_komentarzy where id_zgloszenia ="+id+");")
        conn.commit()
        cur.execute("delete from komentarze where id_komentarza = (select komentarze_id_komentarza from zgloszenia_komentarzy where id_zgloszenia ="+id+");")
        conn.commit()
    if action=="ban":
        ban_duration = request.form["banDuration"];
        ban_reason ="'"+request.form["banReason"]+"'"
        ban_enddate = "CURRENT_DATE"+" + "+ban_duration
        cur.execute("update zgloszenia_komentarzy set czy_rozpatrzony = true where id_zgloszenia = "+id+";")
        conn.commit()
        cur.execute("insert into blokady values (default,CURRENT_DATE,"+ban_enddate+","+ban_reason+","+id+");")
        conn.commit()
    cur.close()
    conn.close()
    return redirect("/admin")

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
