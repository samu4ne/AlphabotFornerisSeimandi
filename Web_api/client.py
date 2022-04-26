from pickle import TRUE
from random import random
import time
from flask import Flask, render_template, redirect, url_for, request, jsonify
import requests
import random

url= 'http://192.168.0.137:5000/api/v1/sensors/obstacles'

def main():
    
    while True:
        #sensori[0]= destra, sensore[1]=sinistra
        http = requests.get(url)
        sensori= http.json()
        print(sensori)

        if sensori[0]==1 and sensori[1]==1:
            #avanti

            destra = -30
            sinistra = 30
        elif sensori[0]==0 and sensori[1]==1:
            #destra
            destra = 0
            sinistra = -30
        elif sensori[0]==1 and sensori[1]==0:
            #sinistra
            destra = 30
            sinistra = 0
        elif sensori[0]==0 and sensori[1]==0:
            #indietro
            if random.randint(0,1)==0:
                destra = 20
                sinistra = -30
            else:
                destra = 30
                sinistra = -20
        else:
            #stop
            destra=0
            sinistra=0

        http = requests.get(f"http://192.168.0.137:5000/api/v1/motors/both?pwmR={destra}&pwmL={sinistra}&tempo={0.2}")
        time.sleep(0.2)
        

if __name__=="__main__":
    main()