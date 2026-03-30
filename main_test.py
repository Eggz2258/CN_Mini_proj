from socket import *
from json import loads
import pickle
from datetime import datetime
host = "0.0.0.0"
port = 5005

buffer_size = 2048

sock = socket(AF_INET,SOCK_DGRAM)

sock.bind((host,port))
class Client:
    client_names = []
    
    def __init__(self,addr):
        self.addr = addr
    def enc(self,message):
        dic = {self.name: message}
        dic = pickle.dumps(dic)
        dic = dic.encode('utf-8')
        return dic
    def send(self,message):
        sock.sendto(message,self.addr)
    @staticmethod
    def stream(raw_data):
        print('streamdata')
        decoded_dict =Client.decode_dict(raw_data)
       
        file = open('recv.wav','ab')
        file.write(decoded_dict['Data'])
        file.close()
        #print(decoded_dict['Data'])

    @staticmethod
    def sendall(message):
        
        for client in Client.client_names:
            print(len(Client.client_names))
            client.send(message)
    @staticmethod
    def decode_dict(data):
        #data = data.decode('utf-8')
        data = pickle.loads(data)
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
        print('through: ',throughput)
#        print(f'total time: {Total_time:.6}' )
#
    @staticmethod
    def recv_message(raw_data):
        data = Client.decode_dict(raw_data)
        Client.logger(data)
        res = data['Message']
        print(data)
        if 'stream Chunk' not in res:
            Client.sendall(raw_data)
        return res
    @staticmethod
    def recv():
        raw_data, addr = sock.recvfrom(2048)
        if addr not in [a.addr for a in Client.client_names]:
           obj =  Client(addr)
           Client.client_names.append(obj)
        #d = data[0:6].decode('utf-8')
        #
        #print(data.decode('utf-8'))
        #if 'streaM' in d:
        #    Client.stream(data)
        
        res = Client.recv_message(raw_data)
        if 'quit' in res:
            for i in Client.client_names:
                if i.addr == addr:
                    Client.client_names.remove(i)
        if 'stream Chunk' in res:
            Client.stream(raw_data)
print('listening on', host,port)
while True:
    Client.recv()
