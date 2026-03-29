from socket import *
from json import loads
from datetime import datetime
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
    def stream(data):
        print('streamdata')
        file = open('recv.wav','ab')
        file.write(data[10:])
        file.close()
        print(data[10:])

    @staticmethod
    def sendall(message):
        
        for client in Client.client_names:
            print(len(Client.client_names))
            client.send(message)
    @staticmethod
    def decode_dict(data):
        data = data.decode('utf-8')
        data = loads(data)
        return data
    @staticmethod
    def logger(data):

        Current_info  = datetime.now()
        current_time = float(Current_info.strftime('%S.%f'))
        Total_bytes = len(data)
        name = data['Name']
        value = data['Message']
        recv_time =float(data['time'][-9:])
        Total_time = current_time - recv_time
        throughput = Total_bytes / Total_time 


#        print("Ttotab bytes: ",Total_bytes)
#        print('through: ',throughput)
#        print(f'total time: {Total_time:.6}' )
#
    @staticmethod
    def recv_message(data):

        Client.sendall(data)
        data = Client.decode_dict(data)
        Client.logger(data)
        value = data['Message']
        print(data)
        return value
    @staticmethod
    def recv():
        data, addr = sock.recvfrom(1024)
        if addr not in [a.addr for a in Client.client_names]:
           obj =  Client(addr)
           Client.client_names.append(obj)
        d = data[0:6].decode('utf-8')

        print(data.decode('utf-8'))
        if 'streaM' in d:
            Client.stream(data)
        else:
            value = Client.recv_message(data)
            if 'quit' in value:
                for i in Client.client_names:
                    if i.addr == addr:
                        Client.client_names.remove(i)
    
print('listening on', host,port)
while True:
    Client.recv()
