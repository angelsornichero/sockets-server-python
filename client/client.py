import socket
from consts import HOST, PORT
from time import sleep
from sys import exit

def recieve_data(socket):
    data = None
    while not data:
        data = socket.recv(1024)
        data.decode()
    print(data)
    return data

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    
    data = recieve_data(s)
        
    print(data)
    if data == b'IDENTIFY':
       id = input('Introduce tu nombre de usuario: ')    
       s.sendall(id.encode())
    

    data = recieve_data(s)
    if data == b'CLOSE':
        s.sendall('OK'.encode())
        s.close()
        exit(0)



