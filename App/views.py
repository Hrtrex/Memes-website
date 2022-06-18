import os
from flask import Flask, redirect, url_for, render_template, request
from werkzeug.utils import secure_filename
from App import app
import psycopg2
from App.memes import Meme

UPLOAD_FOLDER = 'App/static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}

def get_db_connection():
    conn = psycopg2.connect(host='flask-server.postgres.database.azure.com',
                            database='db',
                            user='hrtrex',
                            password='Jebacdisa_12',
                            sslmode='require')
    return conn

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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
    meme_data = Meme()
    meme_data.get_memes_jbzd(f'{page}')
    return render_template("memy.html", memes = meme_data)

@app.route("/kwejk/", defaults={'page': ''})
@app.route("/kwejk/<page>")
def kwejk(page):
    meme_data = Meme()
    meme_data.get_memes_kwejk(f'{page}')
    return render_template("memy.html", memes = meme_data)

@app.route("/upload", methods=['GET', 'POST'])
def upload_meme():
    if request.method == 'POST':
        if 'file' not in request.files:
            return 'No meme uploaded', 400
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute("insert into memy values (default, %s, '2022-06-18', 1, 'tytul', 'opis', 'kategoria')", (filename,))
            conn.commit()
            cur.close()
            conn.close()
            return 'Meme has been uploaded', 200
    return render_template("test.html")