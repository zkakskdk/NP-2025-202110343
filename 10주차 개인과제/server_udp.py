import socket

HOST = "0.0.0.0"
PORT = 3000
BUF = 1024

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((HOST, PORT))
print("[SERVER] UDP Echo 서버 시작:", HOST, PORT)

while True:
    data, addr = sock.recvfrom(BUF)
    msg = data.decode().strip()
    print(f"[수신] {addr} : {msg}")
    sock.sendto(f"Echo: {msg}".encode(), addr)
