import socket
from consts import HOST, PORT
from sys import exit
import threading

class Client:

    __socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    username = None
    running = True

    def __init__(self):
        self.actions = {
            b"IDENTIFY": self.get_identified,
            b"CLOSE": self.close_by_server
        }

    def run(self):
            self.__socket.connect((HOST, PORT))
            ### Start the program, the server will ask the client to connect
            data = self.recieve_data()
            self.actions[data]()
            data = None
            ###
            ### Create a thread for listening new messages and another for writing
            self.write_thread = threading.Thread(target=self.writing_data)
            self.read_thread = threading.Thread(target=self.listen_for_data)
            self.write_thread.start()
            self.read_thread.start()
            ###
            
                
    def listen_for_data(self):
        with self.__socket:
            while self.running == True:
                data = self.__socket.recv(1024)
                data.decode()      
                if data in self.actions:
                    self.actions[data]()
                    continue
                msg = data.decode()
                print(f"\n{msg}\nYou ~> ", end='')
    
    def writing_data(self):
        with self.__socket:
            while self.running == True:
                    message_to_send = input('You ~> ')
                    if self.running == False: break 
                    self.__socket.send(f'{self.username}:{message_to_send}'.encode())
                    

    def recieve_data(self):
        data = None
        while not data:
            data = self.__socket.recv(1024)
            data.decode()
            
        return data

    def get_identified(self):
        id = input('Introduce tu nombre de usuario: ')    
        self.__socket.sendall(id.encode())
        self.username = id

    def close_by_server(self): 
        self.__socket.sendall('OK'.encode())
        self.__socket.close()
        self.running = False
        print("\n[!] Conexion finalizada por el servidor, pulsa enter")
        exit(0)



if __name__ == '__main__':
    client = Client()
    client.run()
