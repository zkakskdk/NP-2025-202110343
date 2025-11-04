import socket
import sys

SERVER_IP = input("서버 IP : ")
SERVER_PORT = 5002
ENC = "utf-8"

with socket.create_connection((SERVER_IP, SERVER_PORT), timeout=5) as s:
    print(s.recv(4096).decode(ENC), end="")
    for line in sys.stdin:
        s.sendall(line.encode(ENC))
        resp = s.recv(4096)
        if not resp:
            break
        text = resp.decode(ENC)
        print(text, end="")
        if text.strip().lower() == "bye":
            break
