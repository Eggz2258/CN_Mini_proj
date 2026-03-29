import socket
from threading import Thread
from time import sleep
from json import dumps
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
        return
    def enc(self,message):
        dic = {self.name: message}
        dic = dumps(dic)
        dic = dic.encode('utf-8')
        return dic
    def send(self):
        while True:
            sleep(0.1)
            message = input("message: ")
            d = self.enc(message)
            sock.sendto(d,Server.addr)
    def recv(self):
        while True:
            data, _ = sock.recvfrom(1024)
            data = data.decode('utf-8')
            print("recv: ",data)

    def start(self):
        Thread(target = self.send).start()
        Thread(target = self.recv).start()

Name = input("Enter your name: ")
server = Server(Name)
print("server started...")
server.start()

while True:
    pass
