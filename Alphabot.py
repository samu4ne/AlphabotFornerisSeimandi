#server tpc

import socket as sck
import threading as thr
import time
import RPi.GPIO as GPIO
import sqlite3 #libreria data base





lista_client = []

#classe thread
class Classe_Thread(thr.Thread):
    #funzione che si avvia alla creazione della classe
    def __init__(self, connessione, indirizzo ,alphabot):
        thr.Thread.__init__(self)   #costruttore super (java)
        self.connessione = connessione
        self.indirizzo=indirizzo
        self.alphabot=alphabot          #per usare la classe del robot all'interno del thread
        self.running = True

    #funzione che si avvia con il comando start()
    def run(self):
        con = sqlite3.connect('./DataBaseRaspeberry.db')        #apro il file database
    
        cur = con.cursor()
        while self.running:     #ciclo infinito del programma
            messaggio = (self.connessione.recv(4096)).decode()          #ricevo il comando

            if messaggio == 'exit':             #per chiudere il programma e scollegare i client
                self.running = False

                lista_client.remove(self)
                
            else:
                print(messaggio)
       
                Nome=messaggio
                for row in cur.execute(f"SELECT Sequenza FROM Movimenti WHERE Nome ='{Nome}'").fetchall():  #leggo all'interno db la stringa corrispondente alla chiave presa in input
                    print(row)      
                
                
                #comandi,tempo,comando,tempo,comando,tempo
              
                vect=row[0].split(',') #splitto i vari comandi e il tempo

                for k in range (0,len(vect)):    #ciclo sul vettore splittato in precedenza
                    #in base a che comando c'è scritto sul db faccio muovere il robot per tot secondi
                    if(vect[k].upper()=="W"):
                        self.alphabot.forward()
                        time.sleep(float(vect[k+1]))        #durata del movimento
                    if(vect[k].upper()=="D"):
                        self.alphabot.right()
                        time.sleep(float(vect[k+1]))
                    if(vect[k].upper()=="S"):
                        self.alphabot.backward()
                        time.sleep(float(vect[k+1]))
                    if(vect[k].upper()=="A"):
                        self.alphabot.left()
                        time.sleep(float(vect[k+1]))
                    if(vect[k].upper()=="STOP"):
                        self.alphabot.stop()

                    k=+1


class AlphaBot(object):  #classe dell'Alfabot
    
    def __init__(self, in1=13, in2=12, ena=6, in3=21, in4=20, enb=26):
        self.IN1 = in1
        self.IN2 = in2
        self.IN3 = in3
        self.IN4 = in4
        self.ENA = ena
        self.ENB = enb
        self.PA  = 20  #velocità in girare
        self.PB  = 20   #velocità per girare

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

    def forward(self, speed=60):  #avanti a velocità 60
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

    def backward(self , speed=60):   #indietro velocità 60
        self.PWMA.ChangeDutyCycle(speed)
        self.PWMB.ChangeDutyCycle(speed)
        GPIO.output(self.IN1, GPIO.LOW)
        GPIO.output(self.IN2, GPIO.HIGH)
        GPIO.output(self.IN3, GPIO.HIGH)
        GPIO.output(self.IN4, GPIO.LOW)
        
        

    def left(self):     #girare a sinistra velocità settata in precedenza
        self.PWMA.ChangeDutyCycle(self.PA)
        self.PWMB.ChangeDutyCycle(self.PB)
        GPIO.output(self.IN1, GPIO.LOW)
        GPIO.output(self.IN2, GPIO.HIGH)
        GPIO.output(self.IN3, GPIO.LOW)
        GPIO.output(self.IN4, GPIO.HIGH)

    def right(self):    #destra con la velocità settata in precedenza
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

def main():
    s = sck.socket(sck.AF_INET, sck.SOCK_STREAM) 
    s.bind(('0.0.0.0', 3450))       #bind del server tcp
    s.listen()
    Ab= AlphaBot()      #inizzializo alphabot


    while True:
        connessione, indirizzo = s.accept()   #connessioni dei client
        

        client = Classe_Thread(connessione, indirizzo, Ab)
        lista_client.append(client)
        client.start()                  #parte la running con il codice +


        #chiusura di tutti i client con running = False
        for k in lista_client:
            if k.running != True:
                k.connessione.close()
                k.join()
                lista_client.remove(k)

    s.close()
    con.close()

main()