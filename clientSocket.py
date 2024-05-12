import socket
import threading
import re


def get_command(message):
    return message.split(",")[0].split(":")[1]


def get_value_of_key(message, key):
    pattern = re.compile(key + r'([^,]+)')
    match = pattern.search(message)
    if match:
        return match.group(1)
    else:
        return None


class ClientSocket:
    def __init__(self):
        self.my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.my_socket.connect(("127.0.0.1", 8888))
        self.player_role = -1
        clientThread = threading.Thread(target=self.__receive__)
        clientThread.start()

    def __send__(self,message):
        self.my_socket.sendall(message)


    def handle_client_message(self, message):
        command = get_command(message)
        print('message:%s' % message)
        print('command:%s' % command)
        print('role:%s' % get_value_of_key(message, "role:"))

        if (command == "start"):
            self.player_role = get_value_of_key(message, "role:")

        print(self.player_role)


        if message[0] == 2:
            print("white move", message)


    def __receive__(self):
        while True:
            message = self.my_socket.recv(1024).decode('utf-8')
            self.handle_client_message(message)

    def __close__(self,message):
        self.my_socket.close()


