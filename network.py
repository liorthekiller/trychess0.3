import socket
import pickle
import random

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind(("127.0.0.1", 8888))
server.listen(10)

client_1, client_1_addr = server.accept()
print(client_1_addr)
client_2, client_2_addr = server.accept()
print(client_2_addr)
# client_1.send("0".encode())
# client_2.send("1".encode())

role_1 = 0
role_2 = 0
flip = random.randint(0, 1)
if flip == 0:
    role_1 = 1
else:
    role_2 = 1

print('command:"start", role:%d' % role_1)

client_1.send(('command:"start", role:"%d"' % role_1).encode())
client_2.send(('command:"start", role:"%d"' % role_2).encode())
# client_1.send('black'.encode())
# client_2.send('white'.encode())


while True:
    res = client_1.recv(16)
    # print(res)
    try:
        print(pickle.loads(res))
    except:
        print("Failed to read")

    client_2.send(res)

    res = client_2.recv(16)
    # print(res)
    try:
        print(pickle.loads(res))
    except:
        print("Failed to read")

    client_1.send(res)