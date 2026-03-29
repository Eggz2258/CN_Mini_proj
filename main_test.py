from socket import *
from json import loads

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
        
        for client in Client.client_names:
            print(len(Client.client_names))
            client.send(message)

    @staticmethod
    def recv():
        data, addr = sock.recvfrom(1024)
        if addr not in [a.addr for a in Client.client_names]:
           obj =  Client(addr)
           Client.client_names.append(obj)
        Client.sendall(data)
        data = data.decode('utf-8')
        data = loads(data)
        name = list(data.keys())[0]
        value = list(data.values())[0]


        if 'quit' in value:
            for i in Client.client_names:
                if i.addr == addr:
                    Client.client_names.remove(i)
        print(data)


print('listening on', host,port)
while True:
    Client.recv()
