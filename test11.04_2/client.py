import socket

class NEchoClient:
    def __init__(self, host, port=2500):
        self.host = host
        self.port = port

    def send_message(self, n, msg):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.host, self.port))
            s.send(f"{n} {msg}".encode())

            response = s.recv(1024).decode()

            response = response.strip()

            print("[서버 응답]")
            print(response)

if __name__ == "__main__":
    ip = input("서버 IP 입력: ")
    client = NEchoClient(ip)
    n = int(input("반복 횟수 입력: "))
    msg = input("메시지 입력: ")
    client.send_message(n, msg)
