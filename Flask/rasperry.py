from http.client import OK
from pickle import FALSE, TRUE
from urllib.parse import uses_params
from flask import Flask, render_template, redirect, url_for, request, make_response
import sqlite3
import random as rm
import RPi.GPIO as GPIO
import datetime
import time



app = Flask(__name__) #si crea l'appicazione

class AlphaBot(object):  #classe dell'Alfabot
    
    def __init__(self, in1=13, in2=12, ena=6, in3=21, in4=20, enb=26):
        self.IN1 = in1
        self.IN2 = in2
        self.IN3 = in3
        self.IN4 = in4
        self.ENA = ena
        self.ENB = enb
        self.PA  = 30  #velocita' in girare
        self.PB  = 30   #velocita' per girare

        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.IN1, GPIO.OUT)
        GPIO.setup(self.IN2, GPIO.OUT)
        GPIO.setup(self.IN3, GPIO.OUT)
        GPIO.setup(self.IN4, GPIO.OUT)
        GPIO.setup(self.ENA, GPIO.OUT)
        GPIO.setup(self.ENB, GPIO.OUT)
        self.PWMA = GPIO.PWM(self.ENA,500)
        self.PWMB = GPIO.PWM(self.ENB,500)
        self.PWMA.start(self.PA)
        self.PWMB.start(self.PB)
        self.stop()

    def forward(self, speed=60):  #avanti a velocita' 60
        self.PWMA.ChangeDutyCycle(speed)
        self.PWMB.ChangeDutyCycle(speed)
        GPIO.output(self.IN1, GPIO.HIGH)
        GPIO.output(self.IN2, GPIO.LOW)
        GPIO.output(self.IN3, GPIO.LOW)
        GPIO.output(self.IN4, GPIO.HIGH)


        
    def stop(self):     #fermare i motori
        self.PWMA.ChangeDutyCycle(0)
        self.PWMB.ChangeDutyCycle(0)
        GPIO.output(self.IN1, GPIO.LOW)
        GPIO.output(self.IN2, GPIO.LOW)
        GPIO.output(self.IN3, GPIO.LOW)
        GPIO.output(self.IN4, GPIO.LOW)

    def backward(self , speed=60):   #indietro velocita' 60
        self.PWMA.ChangeDutyCycle(speed)
        self.PWMB.ChangeDutyCycle(speed)
        GPIO.output(self.IN1, GPIO.LOW)
        GPIO.output(self.IN2, GPIO.HIGH)
        GPIO.output(self.IN3, GPIO.HIGH)
        GPIO.output(self.IN4, GPIO.LOW)
        
        

    def left(self):     #girare a sinistra velocita' settata in precedenza
        self.PWMA.ChangeDutyCycle(self.PA)
        self.PWMB.ChangeDutyCycle(self.PB)
        GPIO.output(self.IN1, GPIO.LOW)
        GPIO.output(self.IN2, GPIO.HIGH)
        GPIO.output(self.IN3, GPIO.LOW)
        GPIO.output(self.IN4, GPIO.HIGH)

    def right(self):    #destra con la velocita' settata in precedenza
        self.PWMA.ChangeDutyCycle(self.PA)
        self.PWMB.ChangeDutyCycle(self.PB)
        GPIO.output(self.IN1, GPIO.HIGH)
        GPIO.output(self.IN2, GPIO.LOW)
        GPIO.output(self.IN3, GPIO.HIGH)
        GPIO.output(self.IN4, GPIO.LOW)
        
    def set_pwm_a(self, value):
        self.PA = value
        self.PWMA.ChangeDutyCycle(self.PA)

    def set_pwm_b(self, value):
        self.PB = value
        self.PWMB.ChangeDutyCycle(self.PB)    
        
    def set_motor(self, left, right):
        if (right >= 0) and (right <= 100):
            GPIO.output(self.IN1, GPIO.HIGH)
            GPIO.output(self.IN2, GPIO.LOW)
            self.PWMA.ChangeDutyCycle(right)
        elif (right < 0) and (right >= -100):
            GPIO.output(self.IN1, GPIO.LOW)
            GPIO.output(self.IN2, GPIO.HIGH)
            self.PWMA.ChangeDutyCycle(0 - right)
        if (left >= 0) and (left <= 100):
            GPIO.output(self.IN3, GPIO.HIGH)
            GPIO.output(self.IN4, GPIO.LOW)
            self.PWMB.ChangeDutyCycle(left)
        elif (left < 0) and (left >= -100):
            GPIO.output(self.IN3, GPIO.LOW)
            GPIO.output(self.IN4, GPIO.HIGH)
            self.PWMB.ChangeDutyCycle(0 - left)


myRobot= AlphaBot()

def validate(username, password):   #per controllare l'usarname e la password
    completion = False
    #with sqlite3.connect('static/db.db') as con:
    con = sqlite3.connect('./db.db')
    cur = con.cursor()
    cur.execute("SELECT * FROM Users")
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
    error = None    #serve per far comparire la scritta "la password e' sbagliata"
    if request.method == 'POST':    #se la richiesta non e' un post l'app manda la pagina
        if request.form.get('login') == 'Login':
            username = request.form['username']
            password = request.form['password']
            completion = validate(username, password) #serve per vedere se esiste sia la password che la l'username
            if completion ==False:
                error = 'Invalid Credentials. Please try again.'
            else:
                resp = make_response(redirect(url_for('secret')))
                resp.set_cookie('username', f'{username}')
                return resp
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
                cur.execute("SELECT * FROM Users")
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
                    print(f"utente {username} a stato aggiunto password= {password}")
                    cur.execute(f"INSERT INTO USERS (USERNAME, PASSWORD) VALUES ('{username}', '{password}')").fetchall()#leggo all'interno db la stringa corrispondente alla chiave presa in input 
                    con.commit()
                    
                    resp = make_response(redirect(url_for('secret')))
                    resp.set_cookie('username', f'{username}')
                    return resp

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
            cur.execute(f"INSERT INTO RegistroMovimenti (movimento, data, utente) VALUES ('sinistra', '{datetime.datetime.now()}', '{request.cookies.get('username')}')").fetchall()#leggo all'interno db la stringa corrispondente alla chiave presa in input 
            con.commit()
            myRobot.left()
        elif  request.form.get('w') == 'avanti':  #andare avanti
            cur.execute(f"INSERT INTO RegistroMovimenti (movimento, data, utente) VALUES ('avanti', '{datetime.datetime.now()}', '{request.cookies.get('username')}')").fetchall()#leggo all'interno db la stringa corrispondente alla chiave presa in input 
            con.commit()
            myRobot.forward()
        elif request.form.get('d') == 'destra':   #girare a destra
            cur.execute(f"INSERT INTO RegistroMovimenti (movimento, data, utente) VALUES ('destra', '{datetime.datetime.now()}', '{request.cookies.get('username')}')").fetchall()#leggo all'interno db la stringa corrispondente alla chiave presa in input 
            con.commit()
            myRobot.right()
        elif request.form.get('s') == 'indietro':   #andare indietro
            cur.execute(f"INSERT INTO RegistroMovimenti (movimento, data, utente) VALUES ('indietro', '{datetime.datetime.now()}', '{request.cookies.get('username')}')").fetchall()#leggo all'interno db la stringa corrispondente alla chiave presa in input 
            con.commit()
            myRobot.backward()
        elif request.form.get('t')=='stop':         #per fermare i comandi
            cur.execute(f"INSERT INTO RegistroMovimenti (movimento, data, utente) VALUES ('stop', '{datetime.datetime.now()}', '{request.cookies.get('username')}')").fetchall()#leggo all'interno db la stringa corrispondente alla chiave presa in input 
            con.commit()
            myRobot.stop()
        elif request.form.get('ok') == 'vai':   #quando l'utente schiaccia il pulsante per prendere in input i comandi complessi
            print("vai")
            comando=request.form['complessi']
            cur.execute(f"INSERT INTO RegistroMovimenti (movimento, data, utente) VALUES ('{comando}', '{datetime.datetime.now()}', '{request.cookies.get('username')}')").fetchall()#leggo all'interno db la stringa corrispondente alla chiave presa in input 
            con.commit()
            for row in cur.execute(f"SELECT Sequenza FROM Movimenti WHERE Nome ='{comando}'").fetchall():  #leggo all'interno db la stringa corrispondente alla chiave presa in input
                    print(row)      
                
            #comandi,tempo,comando,tempo,comando,tempo
              
            vect=row[0].split(',') #splitto i vari comandi e il tempo

            for k in range (0,len(vect)):    #ciclo sul vettore splittato in precedenza
                #in base a che comando c'e' scritto sul db faccio muovere il robot per tot secondi
                if(vect[k].upper()=="W"):
                    myRobot.forward()
                    time.sleep(float(vect[k+1]))        #durata del movimento
                if(vect[k].upper()=="D"):
                    myRobot.right()
                    time.sleep(float(vect[k+1]))
                if(vect[k].upper()=="S"):
                    myRobot.backward()
                    time.sleep(float(vect[k+1]))
                if(vect[k].upper()=="A"):
                    myRobot.left()
                    time.sleep(float(vect[k+1]))
                if(vect[k].upper()=="STOP"):
                    myRobot.stop()

                k=+1
            

    elif request.method == 'GET':
        print("attivazione")
        return render_template('sito.html')
    
    return render_template("sito.html")



if __name__== "__main__":
    app.run(debug=True, host='0.0.0.0') #se cambiamo il codice non bisogna rinviare tutto