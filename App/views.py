from time import sleep
from flask import Flask, redirect, url_for, render_template, request, flash, session, jsonify
from App import app
import psycopg2
import psycopg2.extras
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from datetime import date, datetime
from argparse import Namespace
from flask_login import LoginManager, FlaskLoginClient, login_user, logout_user, current_user, login_required
from flask_mail import Mail, Message
from App.memes import Meme
import os


#def get_db_connection():
#    conn = psycopg2.connect(host='flask-server.postgres.database.azure.com',
#                            database='db',
#                            user='hrtrex',
#                            password='Haslo_db',
#                            sslmode='require')
#    return conn

def get_db_connection():
    conn = psycopg2.connect(host='localhost',
                            database='postgres',
                            user='postgres',
                            password='jebacdisa1')
                            
    return conn

@app.route('/memesRanking/sorted/', methods=['POST'])
def zastosuj_filtry():
    s='desc'
    s = request.form.get('sort')
    sorttyp='oceny'
    sorttyp=request.form.get('sorttyp')
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
    if 'id' in session:
     return render_template('komentarz.html', memy=memy,komentarze=komentarze,odpowiedzi=odpowiedzi,oceny=oceny,ileodp=ileodp,user=session['id'])
    return render_template('komentarz.html', memy=memy,komentarze=komentarze,odpowiedzi=odpowiedzi,oceny=oceny,ileodp=ileodp)

@app.route("/wstawkomentarz",methods=['POST'])
def wstawkom():
    if 'loggedin' not in session:
        return redirect("/komentarze")    
    conn = get_db_connection()
    cur = conn.cursor()
    
    idmema = request.form["wstaw komentarz"]
    tresc=request.form["message"]
    cur.execute("insert into komentarze values(default,'"+ tresc+"',current_date,"+str(session['id'])+","+idmema +",null );")
    conn.commit()
    return redirect("/komentarze")
   
@app.route("/")
def home():
    if 'loggedin' in session:
        return render_template('index.html', email=session['email'])
    return render_template("index.html")

@app.route("/<name>")
def user(name):
    return render_template("index.html")

@app.route("/admin")
def getZgloszenia():

    if 'loggedin' not in session:
            return redirect('/')
    if session['type'] !=2:
            return redirect('/')

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

    if 'loggedin' not in session:
            return redirect('/')
    if session['type'] !=2:
            return redirect('/')

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
        cur.execute("delete from oceny_komentarzy where komentarze_id_komentarza in (select id_komentarza from komentarze where memy_id_mema = (select memy_id_mema from zgloszenia_memow where id_zgloszenia ="+id+"));")
        cur.execute("delete from komentarze where memy_id_mema in (select memy_id_mema from zgloszenia_memow where id_zgloszenia ="+id+");")
        cur.execute("delete from oceny_memow where memy_id_mema in (select memy_id_mema from zgloszenia_memow where id_zgloszenia ="+id+");")
        cur.execute("delete from zgloszenia_memow where memy_id_mema in (select memy_id_mema from zgloszenia_memow where id_zgloszenia ="+id+");")
        cur.execute("delete from memy where id_mema = (select memy_id_mema from zgloszenia_memow where id_zgloszenia ="+id+");")
        conn.commit()
    if action=="ban":
        ban_duration = request.form["banDuration"];
        ban_reason ="'"+request.form["banReason"]+"'"
        ban_enddate = "CURRENT_DATE"+" + "+ban_duration
        cur.execute("update zgloszenia_memow set czy_rozpatrzony = true where id_zgloszenia = "+id+";")
        cur.execute("insert into blokady values (default,CURRENT_DATE,"+ban_enddate+","+ban_reason+","+id+");")
        conn.commit()
    cur.close()
    conn.close()
    return redirect("/admin")

@app.route("/adminActionKom", methods=['POST'])
def adminActionKom():

    if 'loggedin' not in session:
            return redirect('/')
    if session['type']!=2:
            return redirect('/')

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
        cur.execute("delete from oceny_komentarzy where komentarze_id_komentarza = (select komentarze_id_komentarza from zgloszenia_komentarzy where id_zgloszenia ="+id+");")
        cur.execute("delete from komentarze where id_komentarza = (select komentarze_id_komentarza from zgloszenia_komentarzy where id_zgloszenia ="+id+");")
        cur.execute("delete from zgloszenia_komentarzy where komentarze_id_komentarza = (select komentarze_id_komentarza from zgloszenia_komentarzy where id_zgloszenia ="+id+");")
        conn.commit()
    if action=="ban":
        ban_duration = request.form["banDuration"];
        ban_reason ="'"+request.form["banReason"]+"'"
        ban_enddate = "CURRENT_DATE"+" + "+ban_duration
        cur.execute("update zgloszenia_komentarzy set czy_rozpatrzony = true where id_zgloszenia = "+id+";")
        cur.execute("insert into blokady values (default,CURRENT_DATE,"+ban_enddate+","+ban_reason+","+id+");")
        conn.commit()
    cur.close()
    conn.close()
    return redirect("/admin")

#MEMES
UPLOAD_FOLDER = 'App/static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/jbzd/", defaults={'page': ''})
@app.route("/jbzd/<page>")
def jbzd():
    meme_data = Meme()
    #meme_data.get_memes_jbzd(f'{page}')
    meme_data.get_memes_jbzd('1')
    meme_data.get_memes_jbzd('2')
    meme_data.get_memes_jbzd('3')
    meme_data.get_memes_kwejk('1')
    meme_data.get_memes_kwejk('2')
    meme_data.get_memes_kwejk('3')
    return meme_data
    #return render_template("memy.html", memes = meme_data)

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
        title = request.form['tytul']
        description = request.form['opis']
        category = request.form['kategoria']
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute("insert into memy values (default, %s, current_date, 1, %s, %s, %s)", (filename, title, description, category))
            conn.commit()
            cur.close()
            conn.close()
            return redirect("/")
    return render_template("test.html")

#REJESTRACJA
@app.route('/register', methods = ['POST', 'GET'])
def register():
    return render_template('register.html')


@app.route('/userPanel', methods = ['POST', 'GET'])
def userP():
   
    
    password = 0
    password2 = 0
    email = 0

    
    if request.method == 'POST':
        register_data = request.form
        n = Namespace(**register_data)
        user_role_test = 0
        if n.login == 'admin':
            user_role_test = 2
        else:
            user_role_test = 1

    
        if n.password != n.password2:
            return f'Wrong password confirmation'

        

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

    if request.method == 'GET':
        return f"FATAL ERROR"


          
#LOGOWANIE

app.secret_key = 'ashdasuidjnascmioajouwenawicnjkac'

@app.route("/profile")
def profile():

        conn = get_db_connection()
        cur = conn.cursor()
        
        global email
        if 'loggedin' not in session:
            return redirect(url_for('login'))

        
        cur.execute('SELECT * FROM uzytkownicy WHERE email = %s', (email,));
        account = cur.fetchone()

        login = account[1]
        email = account[3]
        user_role = account[4]
        joined = account[5]

        cur.close()
        conn.close()

        return render_template("profile.html",account=account,login=login,email=email,user_role=user_role,joined=joined)



@app.route("/login", methods=['GET', 'POST'])
def login():
    
    

    conn = get_db_connection()
    cur = conn.cursor()



   
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        global email
        email = request.form['email']
        password = request.form['password']
 
        
        cur.execute('SELECT * FROM uzytkownicy WHERE email = %s', (email,));
        account = cur.fetchone()
        
        
        
        
 
        if account:
            
            password_ch = account[2]
            if check_password_hash(password_ch, password):
                
                session['loggedin'] = True
                session['id'] = account[0]
                session['email'] = account[3]
                session['type'] = account[4]
                return render_template("index.html",email=email,id=id)

                
                
            else:
                flash('Incorrect email or password')
        else:
            flash('Incorrect email or password')
   
    return render_template('login.html')


@app.route('/logout')
def logout():    
   if 'loggedin' not in session:
            return redirect('/')
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('email', None)
   global email
   del email
   return redirect(url_for('login'))


#RESET HASLA
@app.route('/passwordReset', methods=['GET', 'POST'])
def resetP():

    conn = get_db_connection()
    cur = conn.cursor()


    if request.method == 'POST' and 'email' in request.form and 'old_password' in request.form and 'new_password' in request.form and 'new_password2' in request.form:
        
        email = request.form['email']
        old_password = request.form['old_password']
        new_password = request.form['new_password']
        new_password2 = request.form['new_password2']

        if new_password != new_password2:
            return f"Wrong new password confirmation"


        cur.execute('SELECT * FROM uzytkownicy WHERE email = %s', (email,));
        account = cur.fetchone()
        
        password_test = account[2]
        email_test = account[3]
        hashed_password = generate_password_hash(new_password)
        
        sql = """ UPDATE uzytkownicy
                SET haslo = %s
                WHERE email = %s"""

        if check_password_hash(password_test, old_password):
            cur.execute(sql, (hashed_password, email_test))
        else:
            return f"Wrong old password"


        conn.commit()
        cur.close()
        conn.close()  


    return render_template('passwordReset.html')


#ZMIANA EMAILA
@app.route('/emailReset', methods=['GET', 'POST'])
def emailReset():

    conn = get_db_connection()
    cur = conn.cursor()


    if request.method == 'POST' and 'email' in request.form and 'new_email' in request.form and 'new_email2' in request.form:
        
        email = request.form['email']
        new_email = request.form['new_email']
        new_email2 = request.form['new_email2']

      
        cur.execute('SELECT * FROM uzytkownicy WHERE email = %s', (email,));
        account = cur.fetchone()
        
        test_id = account[0]
        email_test = account[3]
        
        sql = """ UPDATE uzytkownicy
                SET email = %s
                WHERE id_uzytkownika = %s"""

        if new_email == new_email2:
            cur.execute(sql, (new_email, test_id))
        else:
            return f"Wrong new email confirmation"


        conn.commit()
        cur.close()
        conn.close()  


    return render_template('emailReset.html')




#EMAIL VERYFICATION
@app.route('/emailCheck', methods=['GET', 'POST'])
def emailcheck():

    conn = get_db_connection()
    cur = conn.cursor()



    if request.method == 'POST' and 'server' in request.form and 'email' in request.form:
        
        server = request.form['server']
        
        email = request.form['email']
        
        

        cur.execute('SELECT * FROM uzytkownicy WHERE email = %s', (email,));
        account = cur.fetchone()

        password_testing = account[2]

        

        app.config['MAIL_SERVER']= server
        app.config['MAIL_PORT'] = 587
        app.config['MAIL_USERNAME'] = 'e51fed28a86eac'
        app.config['MAIL_PASSWORD'] = '50d9261ab4b694'
        app.config['MAIL_USE_TLS'] = True
        app.config['MAIL_USE_SSL'] = False
        mail = Mail(app)
       
        msg = Message('Password recovery', sender =   'usmiechnij_sie_webapp@gmail.com', recipients = [email])
        msg.body = "Hello. Don't forget your password next time :) Your password is: %s" % password_testing
        mail.send(msg)
        return render_template('login.html')

    return render_template('emailCheck.html')
