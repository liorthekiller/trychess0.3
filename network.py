import socket
import threading


class Server:
    def __init__(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(('0.0.0.0',1729))
        self.server_socket.listen(2)
        self.white_socket , addr = self.server_socket.accept()
        print(addr, "is connected")
        msg = "Welcome white player. We are waiting for black player"
        self.__send__(msg, self.white_socket)
        self.black_socket, addr = self.server_socket.accept()
        print(addr, "is connected")
        msg = "Welcome black player. let's start"
        self.__send__(msg, self.black_socket)
        msg = "START"
        self.__send__(msg, self.white_socket)

    def __send__(self, msg, client_socket):
        client_socket.send(msg.encode())

    def __receive__(self,client_socket):
        while True:
            msg = client_socket.recv(1024)
            print("from socket:", msg)
server = Server()
recv_thread_white = threading.Thread(target=server.__receive__,args=(server.white_socket,))
recv_thread_white.start()
recv_thread_black = threading.Thread(target=server.__receive__,args=(server.black_socket,))
recv_thread_black.start()

while True:

    server.__send__(input("enter text:"),server.white_socket)
    server.__send__(input("enter text:"), server.black_socket)
    server.__send__(input("enter text:"), server.black_socket)