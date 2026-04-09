from socket import *
from json import loads
import pickle
from time import sleep
from threading import Thread
from queue import Queue, Full
from datetime import datetime

host = "0.0.0.0"
port = 5005
buffer_size = 2048

sock = socket(AF_INET,SOCK_DGRAM)
sock.bind((host,port))

stream_start = 0
stream_throughput = 0


#############SOHAM################
log_queue = Queue(maxsize=10)


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
    


    ############################ ME ##################
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

    #############MADHU###################
    def logger(data):
        global stream_start
        global stream_throughput


        Current_info  = datetime.now()
        current_time = float(Current_info.strftime('%S.%f'))
        

        Total_bytes = len(data)
        name = data['Name']
        value = data['Message']
        stream_flag = data['stream_flag']
        

        if value == 'Stream Start':
            stream_start = current_time
            print('stream start',stream_start)
        if value == 'Stream End':
            byt_siz = data['stream_size']
            stream_througput = byt_siz/(stream_start - current_time)
            print('stream through = ', stream_throughput)
        

        ############### ME ###############
        recv_time =float(data['time'][-9:])
        Total_time = current_time - recv_time
        throughput = Total_bytes / Total_time 

        with open('logger.txt', 'a') as logfile:
            logfile.write(str(data))
            logfile.write(f"Throughput:{str(throughput)}\n")
            if data['stream_size']:
                logfile.write(f"\n Stream Throughput: {stream_throughput}")
            logfile.close()
        print('through: ',throughput,'Bytes per sec')


        #print(f'total time: {Total_time:.6}' )
        #print("Ttotab bytes: ",Total_bytes)


    @staticmethod
    def recv_message(raw_data):
        data = Client.decode_dict(raw_data)
        Client.logger(data)
        res = data['Message']
        flag = data['stream_flag']


        print(data)
        if not flag:
            Client.sendall(raw_data)
        return (res,data)



    @staticmethod
    def recv():
        global log_queue
        while True:
            raw_data, addr = sock.recvfrom(2048)
            if addr not in [a.addr for a in Client.client_names]:
                obj =  Client(addr)
                Client.client_names.append(obj)
            res,data = Client.recv_message(raw_data)
            log_queue.put(res)


            while log_queue.full():
                print('queue is wating')
                sleep(1)

            
            if 'quit' in res:
                for i in Client.client_names:
                    if i.addr == addr:
                        Client.client_names.remove(i)
            if data['stream_flag']:
                Client.stream(raw_data)



    @staticmethod
    def consume():
        global log_queue
        while True:
            if log_queue.full():
                log_queue.get()
                print('consumed')
                sleep(5)


print('listening on', host,port)


############SOHAM############
Thread(target = Client.consume).start()


while True:
    Client.recv()
    continue
