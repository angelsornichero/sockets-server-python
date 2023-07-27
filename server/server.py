import socket
from consts import HOST, PORT
from sys import exit
import threading
import time



class Connection:
    alive = True
    nickname = None
    def __init__(self, connection, address):
        self.__connection = connection
        self.address = address

    def start_comunication(self):
        print(f"[*] Connection from {self.address}")
        self.__connection.send('IDENTIFY'.encode())
        data = None
        while not data:
            data = self.__connection.recv(1024)
            
        self.nickname = data.decode()
        print(f'[*] New user: {self.nickname}')
    
    def handle(self):
        with self.__connection:
            self.start_comunication()
            
            while self.alive == True:
                continue
        
    def mysend(self, msg):
        totalsent = 0
        while totalsent < len(msg):
            sent = self.__connection.send(msg[totalsent:])
            if sent == 0:
                raise RuntimeError("socket connection broken")
            totalsent = totalsent + sent 

    def close(self):
        self.__connection.send("CLOSE".encode())
        self.__connection.close()
        self.alive = False

class Server:

    __socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    __connections = []
    __threads = []
    close_event = threading.Event()

    def __init__(self):
        self.__socket.bind((HOST, PORT))
        self.__socket.listen(10)

    def run(self):
            while self.close_event.is_set() == False: 
                    connection, address = self.__socket.accept()
                    client = Connection(connection=connection, address=address)
                    self.__connections.append(client)
                    
                    t = threading.Thread(target=client.handle)
                    t.start()

                    self.__threads.append(t)
                    
            
        

    def get_connections(self):
        return self.__connections

    def close_allconnections(self):
        for connection in self.__connections:
            connection.close()

    def stop(self):  
        self.close_allconnections()
        self.__socket.close()
        self.close_event.set()
        for t in self.__threads:

            t.join()

        exit(0)

if __name__ == '__main__':
    app = Server()
    
    try: 
        app.run()
    except KeyboardInterrupt:
        print('Exiting...')
        app.stop()
        
        
    
