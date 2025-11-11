import socket

PORT = 3000
BUF = 1024

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_ip = input("서버 IP 입력: ").strip()

while True:
    msg = input("메시지(종료:q): ")
    if msg.lower() == "q":
        break

    sock.sendto(msg.encode(), (server_ip, PORT))
    data, _ = sock.recvfrom(BUF)
    print("[서버 응답]", data.decode())
