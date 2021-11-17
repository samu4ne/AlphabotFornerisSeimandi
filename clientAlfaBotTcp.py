import logging
import socket
import threading as thr
import time

registered = False
nickname = ""
SERVER=('192.168.0.128', 3450)
class Receiver(thr.Thread):
    def __init__(self, s): 
        thr.Thread.__init__(self)
        self.running = True 
        self.s = s

    def stop_run(self):
        self.running = False

    def run(self):
        global registered

        while self.running:
            data = self.s.recv(4096).decode()
            
            if data == "OK":
                registered = True
                logging.info(f"\nConnessione avvenuta, registrato. Entrando nella chat mode...")
            
            else:
                logging.info(f"\n{data}")

def main():
    print("Ciao")
    global registered
    global nickname
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(SERVER)

    ricev = Receiver(s)
    ricev.start()

    while True:
        time.sleep(0.2)

        comando = input("Inserisci il comando >>>")

        s.sendall(comando.encode())

        if 'exit' in comando:
            ricev.stop_run()
            logging.info("Disconnessione...")
            break

    ricev.join()
    s.close()

if __name__ == "__main__":
    main()