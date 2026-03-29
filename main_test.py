from socket import *
from json import loads
print("hello")

host = "0.0.0.0"
port = 5005

buffer_size = 1024

sock = socket(AF_INET,SOCK_DGRAM)

sock.bind((host,port))
class Client:
    client_names = []
    
    def __init__(self,addr):
        self.addr = addr
    def enc(self,message):
        dic = {self.name: message}
        dic = dumps(dic)
        dic = dic.encode('utf-8')
        return dic
    def send(self,message):
        sock.sendto(message,self.addr)

    @staticmethod
    def sendall(message):
        d = Client.enc(message)
        message = d.encode('utf-8')
        for client in Client.client_names:
            sock.sendto(message, client)

    @staticmethod
    def recv():
        data, addr = sock.recvfrom(1024)
        data = data.decode('utf-8')
        if addr not in Client.client_names:
            Client.client_names.append(addr)
        data = loads(data)
        Client.sendall(data)
        print(type(data))


print(sock.getsockname()[0])
print('listening on', host,port)
while True:
    Client.recv()
