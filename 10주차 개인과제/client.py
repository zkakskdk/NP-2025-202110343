# client.py
import socket

PORT = 2500
BUF  = 1024

class TCPClient:
    def __init__(self, host: str, port: int = PORT):
        self.host = host
        self.port = port

    def send_and_recv(self, msg: str):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.host, self.port))
            s.sendall(msg.encode())
            data = s.recv(BUF).decode(errors="ignore")
            print("[서버 응답]", data)

if __name__ == "__main__":
    server_ip = input("서버 IP 입력: ").strip()
    client = TCPClient(server_ip)
    while True:
        msg = input("메시지(종료:q): ")
        if msg.lower() == "q":
            break
        client.send_and_recv(msg)
