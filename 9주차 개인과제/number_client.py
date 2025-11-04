import socket

SERVER_IP = input("서버 IP : ")
SERVER_PORT = 5003
ENC = "utf-8"

n = input("숫자를 입력하세요 : ")

with socket.create_connection((SERVER_IP, SERVER_PORT), timeout=5) as s:
    print(s.recv(4096).decode(ENC), end="") 
    s.sendall((n + "\n").encode(ENC))

    chunks = []
    while True:
        data = s.recv(4096)
        if not data:
            break
        chunks.append(data)
    print(b"".join(chunks).decode(ENC))