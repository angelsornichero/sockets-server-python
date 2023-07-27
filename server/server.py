import socket
from consts import HOST, PORT
from sys import exit
import threading




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
    
    def handle(self, connections):
        with self.__connection:
            self.start_comunication()
            
            while self.alive == True:
                data = self.__connection.recv(1024)
                msg = data.decode()
                if ':' in msg == False: continue
                try: 
                    [username, message] = msg.split(':')
                except ValueError:
                    message = ''
                    pass
                
                if data:
                    if message == 'QUIT':
                        self.close()
                        for i in range(0, len(connections) - 1):
                            connection = connections[i]
                            if connection.nickname == username: connections.pop(i)
                            print(connections)
                        self.broadcast(f'{username} has disconnected', 'SYSTEM', connections)
                        continue
                    self.broadcast(message, username, connections)
    
    def broadcast(self, message, username, connections):
        if len(connections) == 0: return
        try:
            for connection in connections:
                if connection.nickname == username: continue
                connection.send(f"{username} ~> {message}".encode())
        except OSError:
            pass
        
    def send(self, msg):
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

    def __init__(self):
        self.__socket.bind((HOST, PORT))
        self.__socket.listen(10)

    def run(self):
            while True: 
                    connection, address = self.__socket.accept()
                    client = Connection(connection=connection, address=address)
                    self.__connections.append(client)
                    
                    t = threading.Thread(target=client.handle, args=[self.__connections])
                    t.start()

                    self.__threads.append(t)
                    
    
        

    def get_connections(self):
        return self.__connections

    def close_allconnections(self):
        print(self.__connections)
        for connection in self.__connections:
            connection.close()

    def stop(self):  
        self.close_allconnections()
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
        
        
    
