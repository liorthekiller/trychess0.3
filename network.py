import socket
import pickle
import random

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind(("192.168.198.70", 8888))
server.listen(10)

client_1, client_1_addr = server.accept()
print(client_1_addr)
client_2, client_2_addr = server.accept()
print(client_2_addr)

# 0 is white, 1 is black
role_1 = 0
role_2 = 0
flip = random.randint(0, 1)
if flip == 0:
    role_1 = 1
else:
    role_2 = 1

print('command:start; role:%d' % role_1)

client_1.send(('command:start; role:%d' % role_1).encode())
client_2.send(('command:start; role:%d' % role_2).encode())

if (role_1 == 0):
    turn_of = 1
else:
    turn_of = 2

while True:
    # each turn we know which players message we are getting.

    if (turn_of == 1):
        res = client_1.recv(1024)
        move = -1
        print('res:%s' % res)

        try:
            move = pickle.loads(res)
            print('res with pickle:%s' % move)
        except:
            print("Failed to read")

        # send client 2 the turn
        # and move the turn to him

        client_2.send(('command:new_move; move:%s' % move).encode())
        print('move sent to client2:%s' % move)
        turn_of = 2
    else:
        res = client_2.recv(1024)
        move = -1
        print('res:%s' % res)

        try:
            move = pickle.loads(res)
            print('res with pickle:%s' % move)
        except:
            print("Failed to read")

        # send client 1 the turn
        # and move the turn to him
        client_1.send(('command:new_move; move:%s' % move).encode())
        print('move sent to client1:%s' % move)
        turn_of = 1

    # res = client_1.recv(1024)
    # # print(res)
    # try:
    #     print(pickle.loads(res))
    # except:
    #     print("Failed to read")
    #
    # client_2.send(res)
    #
    # res = client_2.recv(1024)
    # # print(res)
    # try:
    #     print(pickle.loads(res))
    # except:
    #     print("Failed to read")
    #
    # client_1.send(res)
