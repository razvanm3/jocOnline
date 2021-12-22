from flask import Flask, render_template,request,flash,redirect,url_for
import sqlite3

app = Flask(__name__)
app.secret_key="123"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/add_record')
def add_record():
    return render_template('add_record.html')

@app.route("/addData",methods=["POST","GET"])
def addData():
    if request.method=='POST':
        try:
            cont = request.form['cont']
            numeCaracter=request.form['numeCaracter']
            tipCaracter=request.form['tipCaracter']
            nivel=request.form['nivel']
            bani=request.form['bani']
            con=sqlite3.connect("jocOnlineDB.db")
            cur=con.cursor()
            cur.execute("INSERT INTO tblCaractere(cont,numeCaracter,tipCaracter,nivel,bani)values(?,?,?,?,?)",(cont,numeCaracter,tipCaracter,nivel,bani))
            con.commit()
            flash("Inregistrare adaugata cu succes!","success")
        except:
            flash("Eroare!","danger")
        finally:
            return redirect(url_for("home"))
            con.close()

@app.route('/view_record')
def view_record():
    con=sqlite3.connect("jocOnlineDB.db")
    con.row_factory=sqlite3.Row
    cur=con.cursor()
    cur.execute("SELECT * FROM tblCaractere ORDER BY nivel DESC")
    data=cur.fetchall()
    con.close()
    return render_template("view_record.html",data=data)

@app.route('/update_record/<string:id>',methods=["POST","GET"])
def update_record(id):
    con=sqlite3.connect("jocOnlineDB.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM tblCaractere where IDCaracter=?",(id,))
    data = cur.fetchone()
    con.close()

    if request.method=='POST':
        try:
            numeCaracter = request.form['numeCaracter']
            tipCaracter = request.form['tipCaracter']
            nivel = request.form['nivel']
            bani = request.form['bani']
            con = sqlite3.connect("jocOnlineDB.db")
            cur = con.cursor()
            cur.execute("UPDATE tblCaractere SET numeCaracter=?,tipCaracter=?,nivel=?,bani=? where IDCaracter=?",(numeCaracter,tipCaracter,nivel,bani,id,))
            con.commit()
            flash("Inregistrare modificata cu succes!","success")
        except:
            flash("Eroare!","danger")
        finally:
            return redirect(url_for("home"))
            con.close()
    return render_template('update_record.html',data=data)

@app.route('/delete_record/<string:id>')
def delete_record(id):
    try:
        con = sqlite3.connect("jocOnlineDB.db")
        cur = con.cursor()
        cur.execute("DELETE FROM tblCaractere where IDCaracter=?",(id,))
        con.commit()
        flash("Inregistrare stearsa cu succes!","success")
    except:
        flash("Eroare!","danger")
    finally:
        return redirect(url_for("home"))
        con.close()

if __name__ == '__main__':
    app.run(debug=True)
