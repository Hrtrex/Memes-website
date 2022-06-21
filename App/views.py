from flask import Flask, redirect, url_for, render_template,request
from App import app
from App.db import get_db_connection
import os
import psycopg2
def get_db_connection():
    conn = psycopg2.connect(host='flask-server.postgres.database.azure.com',
                            database='db',
                            user='hrtrex',
                            password='Jebacdisa_12',
                            sslmode='require'
                            )
    return conn
@app.route("/")

def home():
    return render_template("index.html")


@app.route('/memesRanking/sorted/', methods=['POST'])
def zastosuj_filtry():
    s='desc'
    s = request.form.get('sort')
    sorttyp='oceny';
    sorttyp=request.form.get('sorttyp');
    if sorttyp=='oceny':
        ok='Srednia ocen: ' 
    else:
       ok='Liczba komentarzy'
    test=''
    k='Wszystkie'
    k = request.form.get('kat')
    if k!='Wszystkie':
        test=" where kategoria='"+k+"'"
    # dodac order by data dodania
    conn = get_db_connection()
    cur = conn.cursor()
    #qerrys="select id_mema,tytul, nazwa_pliku,kategoria,CAST(avg(jaka_ocena) as NUMERIC(10,1)) srednia from oceny_memow,memy "+ test + "  group by id_mema having avg(jaka_ocena) is not null order by srednia " + s +";"
    qerrys="select id_mema,tytul, nazwa_pliku,kategoria,CAST(avg(jaka_ocena) as NUMERIC(10,1)) srednia,opis from memy inner join oceny_memow on memy.id_mema=oceny_memow.Memy_id_mema "+ test + " group by id_mema having avg(jaka_ocena) is not null order by srednia " + s +";"
    #qerrys="select id_mema,tytul,nazwa_pliku from memy;"
    if sorttyp=='komentarze':
        qerrys="select id_mema,tytul,nazwa_pliku,kategoria,count(id_komentarza) as liczba_kom,opis from komentarze,memy where "+ test+" memy.id_mema=komentarze.Memy_id_mema group by id_mema having count(id_komentarza) is not null order by liczba_kom "+ s +";"
    cur.execute(qerrys)
    memy = cur.fetchall()
    querryc="select distinct kategoria from memy;"
    cur.execute(querryc)
    kategorie = cur.fetchall()
    for i in range(len(kategorie)):
        kategorie[i]=''.join(kategorie[i])
    
    cur.close()
    conn.close()
    return render_template('memesRanking.html', memy=memy, kategorie = kategorie,k=k,sorttyp=sorttyp, ok=ok)
@app.route("/memesRanking/")

   
def domyslne_filtry():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('select id_mema,tytul,nazwa_pliku,kategoria,CAST(avg(jaka_ocena) as NUMERIC(10,1)) srednia,opis from oceny_memow,memy where memy.id_mema=oceny_memow.Memy_id_mema group by id_mema having avg(jaka_ocena) is not null order by srednia desc;')
    memy = cur.fetchall()
    querryc="select distinct kategoria from memy;"
    cur.execute(querryc)
    kategorie = cur.fetchall()
    for i in range(len(kategorie)):
        kategorie[i]=''.join(kategorie[i])
    ok='Srednia ocen'
    sorttyp='oceny'
    cur.close()
    conn.close()
    return render_template('memesRanking.html', memy=memy, kategorie=kategorie,sorttyp=sorttyp, ok=ok)
@app.route("/<name>")

def user(name):
    return render_template("index.html")

#def user(name):
    

#    return render_template("index.html")

@app.route("/admin")
def admin():
    return redirect(url_for("home"))

@app.route("/jbzd/<page>")
def jbzd():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)