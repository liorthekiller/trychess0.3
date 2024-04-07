import socket
import threading


class CLientSocket:
    def __init__(self):
        self.my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.my_socket.connect(("127.0.0.1", 8888))
        clientThread = threading.Thread(target=self.__receive__)
        clientThread.start()

    def __send__(self,message):
        self.my_socket.sendall(message)

    def __receive__(self):
        while True:
            message = self.my_socket.recv(16).decode('utf-8')
            print(message)
            if message[0] == 2:
                print("white move", message)

    def __close__(self,message):
        self.my_socket.close()
