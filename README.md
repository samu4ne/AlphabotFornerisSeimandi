# Alphabot
Progetto eseguito da Forneris Samuele, [Seimandi Alessandro](https://github.com/AleSeima)

L'Alphabot viene comandato da remoto, attraverso un client e server con tecnologia tcp.

Una volta che il server ha ricevuto i messaggi con le azioni e li ha interpretati, si utilizza la libreria RPi.GPIO grazie alla quale è possibile comandare i motori elettrici attraverso il raspberry.


<img width="524" alt="Schermata 2021-11-18 alle 08 15 17" src="https://user-images.githubusercontent.com/72200914/142370148-4eec84f4-447b-46c3-8e0f-6cc60ebd5bfe.png">


## Implementazione con un DataBase
Una volta che il server (Raspberry) ha ricevuto i messaggi, li interpreta, cercandoli all'interno del DataBase, e per farlo abbiamo utilizzato la libreria di Python sqlite3, azionando così i motori per un tot di secondi.

Nel database sono presenti i possibili comandi da far eseguire al robot, questi possono essere semplici come destra, sinistra.., o più complessi come fargli percorrere un otto o uno zig zag

#### Nel database sono presenti tre sezioni:

ID: numero del comando

NAME: denominazione del comando

SEQUENZA: qui sono presenti le serie di operazioni per far eseguire il comando completo indicato nella sezione NAME. 

LETTERE: indicano la direzione in cui far muovere l'Alphabot, dettata da WASD (avanti, sinistra, indietro, destra)

NUMERI: indicano la durata della direzione da mantenere (ovvero della lettera che precede il numero)

![Schermata da 2021-11-18 08-22-19](https://user-images.githubusercontent.com/72200995/142370591-e9a728ca-1074-4783-8329-a5c3b1e6e8c5.png)

