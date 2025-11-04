import socket

SERVER_IP = input("서버 IP : ")
SERVER_PORT = 5001
ENC = "utf-8"

with socket.create_connection((SERVER_IP, SERVER_PORT), timeout=5) as s:
    s.sendall(b"TIME\n")
    data = s.recv(4096)
    print(data.decode(ENC))
