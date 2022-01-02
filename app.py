from flask import Flask, jsonify, render_template, url_for, request, flash, redirect, session
from flask_wtf import *
import sqlite3
from forms import RegistrationForm, LoginForm
from flask_login import login_user, current_user, logout_user, login_required
import hashlib
import datetime


app = Flask(__name__)
app.config['SECRET_KEY'] = '123456789'
def query_db(database, table_name, columns = "*", order_by = None, order="ASC", limit=10, offset=0):
    conn = sqlite3.connect(database)

    querry = ""
    if isinstance(columns, str):
        querry = f"SELECT {columns}"
    elif isinstance(columns, list) or isinstance(columns,tuple):
        querry = f"SELECT "
        for attribute in columns:
            querry += f"{attribute}, "
        querry = querry[:-2]
    querry += f" FROM {table_name}"
    if order_by:
        querry += f" ORDER BY {order_by} {order}"
    querry += f" LIMIT {limit} OFFSET {offset};"

    cursorInst = conn.cursor()
    cursorInst.execute(querry)
    datas = cursorInst.fetchall()
    return datas


@app.route("/home")
@app.route("/")
def hello():
    return render_template("indexUser.html")

@app.route("/conturi")
def conturi():
    offset = request.args.get("offset")
    limit = request.args.get("limit")
    if offset == None:
        offset = 0
    else:
        offset = int(offset)
    if limit == None:
        limit = 10
    else:
        limit = int(limit)
    lastValue = query_db(database="jocOnlineDB.db", table_name="tblConturi", limit=1, offset=0, order_by='rowid', order='DESC')[0][0] - 1000000

    nextOffset = offset + limit
    previousOffset = offset - limit
    lastOffset = lastValue // 10 * 10
    if previousOffset < 0:
        previousOffset = 0
    if nextOffset > lastValue:
        nextOffset = lastValue // 10 * 10

    conturi = query_db(database="jocOnlineDB.db", table_name="tblConturi", limit=limit, offset=offset, order_by='rowid', order='ASC')

    print(lastValue)
    return render_template("conturi.html", conturi = conturi, title='Tabela de Conturi',
    nextOffset = nextOffset, previousOffset = previousOffset, lastOffset = lastOffset)

@app.route("/caractere")
def caractere():
    caractere = query_db(database="jocOnlineDB.db", table_name="tblCaractere", limit=100, offset=0, order_by='nivel', order='DESC' )
    return render_template("caractere.html", caractere = caractere)

@app.route("/misiuni")
def misiuni():
    offset = request.args.get("offset")
    limit = request.args.get("limit")
    if offset == None:
        offset = 0
    else:
        offset = int(offset)
    if limit == None:
        limit = 10
    else:
        limit = int(limit)
    lastValue = query_db(database="jocOnlineDB.db", table_name="tblMisiuni", limit=1, offset=0, order_by='rowid', order='DESC')[0][0] - 3000000

    nextOffset = offset + limit
    previousOffset = offset - limit
    lastOffset = lastValue // 10 * 10
    if previousOffset < 0:
        previousOffset = 0
    if nextOffset > lastValue:
        nextOffset = lastValue // 10 * 10

    misiuni = query_db(database="jocOnlineDB.db", table_name="tblMisiuni", limit=limit, offset=offset, order_by='rowid',order='ASC')

    print(lastValue)
    return render_template("misiuni.html", misiuni=misiuni,
                           nextOffset=nextOffset, previousOffset=previousOffset, lastOffset=lastOffset)

@app.route("/obiecte")
def iteme():
    offset = request.args.get("offset")
    limit = request.args.get("limit")
    if offset == None:
        offset = 0
    else:
        offset = int(offset)
    if limit == None:
        limit = 10
    else:
        limit = int(limit)
    lastValue = query_db(database="jocOnlineDB.db", table_name="tblIteme", limit=1, offset=0, order_by='rowid', order='DESC')[0][0] - 4000000

    nextOffset = offset + limit
    previousOffset = offset - limit
    lastOffset = lastValue // 10 * 10
    if previousOffset < 0:
        previousOffset = 0
    if nextOffset > lastValue:
        nextOffset = lastValue // 10 * 10

    iteme = query_db(database="jocOnlineDB.db", table_name="tblIteme", limit=limit, offset=offset, order_by='rowid',order='ASC')

    print(lastValue)
    return render_template("obiecte.html", iteme=iteme,
                           nextOffset=nextOffset, previousOffset=previousOffset, lastOffset=lastOffset)


@app.route("/caractereUser")
def caractereUser():
    con = sqlite3.connect("jocOnlineDB.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM tblCaractere JOIN tblConturi ON tblCaractere.cont = tblConturi.IDCont WHERE email=? ORDER BY nivel DESC",(session['email'],))
    caractereUser = cur.fetchall()
    con.close()
    return render_template("caractereUser.html", caractereUser=caractereUser)

@app.route('/stergeCaracterUser/<string:id>')
def stergeCaracterUser(id):
    try:
        con = sqlite3.connect("jocOnlineDB.db")
        cur = con.cursor()
        cur.execute("DELETE FROM tblCaractere where IDCaracter=?",(id,))
        con.commit()
        flash("Caracterul tau a fost sters!","success")
    except:
        flash("Eroare!","danger")
    finally:
        return redirect(url_for("hello"))
        con.close()

@app.route('/creeazaCaracterUser')
def add_record():
    return render_template('creeazaCaracterUser.html')

@app.route("/creeazaCaracter",methods=["POST","GET"])
def addData():
    if request.method=='POST':
        try:
            numeCaracter=request.form['numeCaracter']
            tipCaracter=request.form['tipCaracter']
            nivel=1
            bani=0

            con0=sqlite3.connect("jocOnlineDB.db")
            cur0 = con0.cursor()
            cur0.execute("SELECT IDCont FROM tblConturi WHERE email=?",(session['email'],))
            con0.commit()
            cont = cur0.fetchone()

            con0.close()
            con = sqlite3.connect("jocOnlineDB.db")
            cur=con.cursor()
            cur.execute("INSERT INTO tblCaractere(cont,numeCaracter,tipCaracter,nivel,bani)values(?,?,?,?,?)",(cont[0],numeCaracter,tipCaracter,nivel,bani))
            con.commit()
            flash("Caracterul a fost creat!","success")
        except:
            flash("Eroare!","danger")
        finally:
            return redirect(url_for("hello"))
            con.close()

@app.route("/obiecteCaracterUser/<string:id>")
def obiecteCaracterUser(id):
    con = sqlite3.connect("jocOnlineDB.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("SELECT nivelNecesarItem, numeItem, pret FROM tblCaractereIteme JOIN tblIteme ON tblCaractereIteme.IDItem = tblIteme.IDItem WHERE IDCaracter=?",(id,))
    obiecteCaracterUser = cur.fetchall()
    con.close()
    return render_template("obiecteCaracterUser.html", obiecteCaracterUser=obiecteCaracterUser)

@app.route("/misiuniCaracterUser/<string:id>")
def misiuniCaracterUser(id):
    con = sqlite3.connect("jocOnlineDB.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("SELECT numeMisiune, nivelRecomandat, recompensa FROM tblCaractereMisiuni JOIN tblMisiuni ON tblCaractereMisiuni.IDMisiune = tblMisiuni.IDMisiune WHERE IDCaracter=?",(id,))
    misiuniCaracterUser = cur.fetchall()
    con.close()
    return render_template("misiuniCaracterUser.html", misiuniCaracterUser=misiuniCaracterUser)


######## RADU

@app.route("/submitlogin", methods=['POST'])
def submit_login():
    email = request.form['email']
    password = request.form['password']

    conn = sqlite3.connect("jocOnlineDB.db")
    querry = f"SELECT * FROM tblConturi WHERE email = '{email}';"
    cursorInst = conn.cursor()
    cursorInst.execute(querry)
    data = cursorInst.fetchone()
    print(data)
    if data:
        hash_db = data[4]
        hash_input = hashlib.md5(password.encode()).hexdigest()
        if hash_db == hash_input:
            session['email'] = data[1]
            return redirect('/home')
        else:
            flash("ERRORS")
            return redirect('/home')
    else:
        flash("ERRORS")
        return redirect('/home')

@app.route("/logout")
def logout():
    session.pop('email',None)
    return redirect("/home")

@app.route("/register")
def register():
    return render_template('register.html')

@app.route("/submitregister", methods=['POST'])
def submit_register():
    email = request.form['email']
    birth_date = request.form['birth-date']
    account_date = str(datetime.date.today())
    password = request.form['password']
    password_confirm = request.form['password-confirm']

    conn = sqlite3.connect("jocOnlineDB.db")
    querry = f"SELECT * FROM tblConturi WHERE email = '{email}';"
    cursorInst = conn.cursor()
    cursorInst.execute(querry)
    data = cursorInst.fetchone()

    if data:
        flash("Email deja folosit")
        return redirect('/register')
    elif password_confirm != password:
        flash("Parolele nu coincid")
        return redirect('/register')
    else:
        birth_date_obj = datetime.datetime.strptime(birth_date, "%Y-%m-%d").date()
        actual_date = datetime.date.today()
        if (actual_date - birth_date_obj).days < 365 *18:
            flash("Varsta mai mica de 18 ani")
            return redirect('/register')
        else:
            password_hash = hashlib.md5(password.encode()).hexdigest()
            id = query_db(database="jocOnlineDB.db", table_name="tblConturi", columns='*',order='DESC',order_by='IDCont',limit=1)[0][0] + 1
            query = f"INSERT INTO tblConturi VALUES({id},'{email}','{birth_date}','{account_date}','{password_hash}');"
            conn = sqlite3.connect("jocOnlineDB.db")
            cursorInst = conn.cursor()
            cursorInst.execute(query)
            conn.commit()
            conn.close()
            flash("You can now log in")
            return redirect('/home')


@app.route("/resetpassword")
def resetpassword():
    return render_template('resetpassword.html')

@app.route("/submitreset", methods=['POST'])
def submit_reset():
    email = request.form['email']


if __name__ == '__main__':
    app.run(debug=True, host = "0.0.0.0", port=5000)

