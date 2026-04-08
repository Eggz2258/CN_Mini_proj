import socket
from threading import Thread
from time import sleep
from json import dumps,loads
import pickle
from datetime import datetime
# Define the target IP address and port
UDP_IP = '255.255.255.255'
UDP_PORT = 5005
MESSAGE = b"Hello, World!"

# Create the UDP socket
sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP

sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
class Server:
    sock = sock
    addr = (UDP_IP,UDP_PORT)
    def __init__(self,name):
        self.name = name
        self.flag = True
        
    def enc(self,message, data = None, stream_flag = False,siz = None):
        now = datetime.now()
        dic = {'Name': self.name,'Message': message,'time': now.strftime('%H:%M:%S.%f'), 'Date':now.strftime('%d-%m-%Y'), 'Data' :data, 'stream_flag': stream_flag,'stream_size' : siz}
        dic = pickle.dumps(dic)
        #dic = dic.encode('utf-8')
        data = None
        return dic
    def send(self,message = None):
        while self.flag:
            sleep(0.1)
            if message == None:
                message = input("message: ")
            if "quit" in message:
                self.flag = False
            if message == 's':
                self.stream()
                message = None
                continue
            d = self.enc(message)
            sock.sendto(d,Server.addr)
            message = None
    def recv(self):
        while self.flag:
            data, _ = sock.recvfrom(2048)
            #data = data.decode('utf-8')
            data = pickle.loads(data)

            name = data['Name']
            value = data['Message']

            print(f"{name}: {value}")

    def start(self):
        self.sender = Thread(target = self.send)
        self.recver = Thread(target = self.recv)
        self.sender.start()
        self.recver.start()

    def stream(self):
        file = open('./aud.wav', 'rb')
        data = file.read()
        prev = 0
        sock.sendto(self.enc('Stream Start'), Server.addr)
        for chunk in range(1024,len(data)+1024,1024):
            print('sending chunk',chunk/1024,'...')
            meta = self.enc(f'stream Chunk {chunk/1024}', data =data[prev:chunk],stream_flag = True)
            meow = meta
            sleep(0.01)

            sock.sendto(meow,Server.addr)
            prev += 1024
        sock.sendto(self.enc('Stream End',siz = chunk), Server.addr)

Name = input("Enter your name: ")
server = Server(Name)
print("server started...")
server.start()

while server.flag:
    pass

sock.close()
