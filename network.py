import socket
import pickle

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind(("0.0.0.0", 8888))
server.listen(10)

client_1, client_1_addr = server.accept()
print(client_1_addr)
client_2, client_2_addr = server.accept()
print(client_2_addr)

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