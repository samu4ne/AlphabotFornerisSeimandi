from http.client import OK
from pickle import FALSE, TRUE
from urllib.parse import uses_params
from flask import Flask, render_template, redirect, url_for, request
import sqlite3
import random as rm
import datetime




app = Flask(__name__) #si crea l'appicazione

def validate(username, password):   #per controllare l'usarname e la password
    completion = False
    #with sqlite3.connect('static/db.db') as con:
    con = sqlite3.connect('./db.db')
    cur = con.cursor()
    cur.execute("SELECT * FROM USERS")
    rows = cur.fetchall()
    for row in rows:
        dbUser = row[0]
        dbPass = row[1]
        if dbUser==username:
            completion=check_password(dbPass, password)
    return completion

def check_password(hashed_password, user_password):
    return hashed_password == user_password

@app.route('/', methods=['GET', 'POST'])
def login():
    con = sqlite3.connect('./db.db')
    cur = con.cursor()
    error = None    #serve per far comparire la scritta "la password è sbagliata"
    if request.method == 'POST':    #se la richiesta non è un post l'app manda la pagina
        if request.form.get('login') == 'Login':
            username = request.form['username']
            password = request.form['password']
            completion = validate(username, password) #serve per vedere se esiste sia la password che la l'username
            if completion ==False:
                error = 'Invalid Credentials. Please try again.'
            else:
                print(datetime.datetime.now())
                cur.execute(f"INSERT INTO Accessi (nomeUtente, data) VALUES ('{username}', '{datetime.datetime.now()}')").fetchall()#leggo all'interno db la stringa corrispondente alla chiave presa in input 
                con.commit()
                return redirect(url_for('secret')) #url_for prende una nome di una funzione, e ritorna il suo URL
        elif request.form.get('sign up') == 'Sign up':
            return redirect(url_for('iscrizione'))

    return render_template('login.html', error=error)   #ti porta alla pagina segreta


@app.route('/iscrizione', methods=['GET', 'POST'])
def iscrizione():
    error = None    #serve per far comparire la scritta "la password e' sbagliata"
    if request.method=='POST':
        con = sqlite3.connect('./db.db')
        cur = con.cursor()


        if request.form.get('sign up') == 'Sign up':  
            username = request.form['username']
            password = request.form['password']
            password2= request.form['Confirm password']
            #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!aggiungere se si riesce il controllo per vedere se ci sono tutti i campi
   
            if password==password2: 
                cur.execute("SELECT * FROM USERS")
                rows = cur.fetchall()
                ok=True #variabile per vedere se l'usarnema e' gia' in uso
                for row in rows:
                    dbUser = row[0]
                    if dbUser==username:
                        print(dbUser)
                        print(username)
                        ok=FALSE

                if ok!=True:
                    error = 'Utente gia in uso.'
                else:
                    print(f"utente {username} e stato aggiunto password= {password}")
                    cur.execute(f"INSERT INTO USERS (USERNAME, PASSWORD) VALUES ('{username}', '{password}')").fetchall()#leggo all'interno db la stringa corrispondente alla chiave presa in input 
                    con.commit()

                    return redirect(url_for('secret')) #url_for prende una nome di una funzione, e ritorna il suo URL

            else:   #le due passord inserite sono sbagliate
                error = 'Le due password non corrispondono'

    if request.method=='GET':
        print("iscrizione")
        return render_template('iscrizione.html')
    
    return render_template("iscrizione.html", error=error)
        


@app.route('/secret' ,methods=['GET', 'POST'])         # pagina che puoi accedere solo con il nome utente e la password
def secret():

    con = sqlite3.connect('./db.db')
    cur = con.cursor()

    if request.method == 'POST':
        print(request.form.get('action1'))
        if request.form.get('a') == 'sinistra': #girare a sinistra
            cur.execute(f"INSERT INTO RegistroMovimenti (movimento, data) VALUES ('sinistra', '{datetime.datetime.now()}')").fetchall()#leggo all'interno db la stringa corrispondente alla chiave presa in input 
            con.commit()
            print("sinistra")
        elif  request.form.get('w') == 'avanti':  #andare avanti
            cur.execute(f"INSERT INTO RegistroMovimenti (movimento, data) VALUES ('avanti', '{datetime.datetime.now()}')").fetchall()#leggo all'interno db la stringa corrispondente alla chiave presa in input 
            con.commit()
            print("avanti")
        elif request.form.get('d') == 'destra':   #girare a destra
            cur.execute(f"INSERT INTO RegistroMovimenti (movimento, data) VALUES ('destra', '{datetime.datetime.now()}')").fetchall()#leggo all'interno db la stringa corrispondente alla chiave presa in input 
            con.commit()
            print("destra")
        elif request.form.get('s') == 'indietro':   #andare indietro
            cur.execute(f"INSERT INTO RegistroMovimenti (movimento, data) VALUES ('indietro', '{datetime.datetime.now()}')").fetchall()#leggo all'interno db la stringa corrispondente alla chiave presa in input 
            con.commit()
            print("indietro")
        elif request.form.get('ok') == 'vai':
            print("vai")
            comando=request.form['complessi']
            cur.execute(f"INSERT INTO RegistroMovimenti (movimento, data) VALUES ('{comando}', '{datetime.datetime.now()}')").fetchall()#leggo all'interno db la stringa corrispondente alla chiave presa in input 
            con.commit()
            print(comando)

    elif request.method == 'GET':
        print("attivazione")
        return render_template('sito.html')
    
    return render_template("sito.html")

if __name__== "__main__":
    app.run(debug=True, host='0.0.0.0') #se cambiamo il codice non bisogna rinviare tutto