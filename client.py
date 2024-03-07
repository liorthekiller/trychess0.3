import socket
import threading


class Client:
    def __init__(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect(('127.0.0.1',1729))

    def __send__(self,msg):
        self.client_socket.send(msg.encode())

    def __receive__(self):
        msg = self.client_socket.recv(1024)
        print(msg)
        # return msg.decode()

client = Client()
recv_thread = threading.Thread(target=client.__receive__)
recv_thread.start()
# while True:
#     client.__send__(input("enter message:"))