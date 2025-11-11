# server.py
import socket
import threading

HOST = "0.0.0.0"
PORT = 2500
BUF  = 1024

class ClientHandler(threading.Thread):
    def __init__(self, conn: socket.socket, addr):
        super().__init__(daemon=True)
        self.conn = conn
        self.addr = addr

    def run(self):
        print(f"[+] 연결됨: {self.addr}")
        try:
            while True:
                data = self.conn.recv(BUF)
                if not data:
                    break
                msg = data.decode(errors="ignore")
                print(f"[{self.addr}] 수신: {msg.strip()}")
                self.conn.sendall(f"Echo: {msg}".encode())
        except Exception as e:
            print(f"[!] 예외: {self.addr} {e}")
        finally:
            self.conn.close()
            print(f"[-] 종료: {self.addr}")

class TCPServer:
    def __init__(self, host=HOST, port=PORT):
        self.host = host
        self.port = port

    def start(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((self.host, self.port))
            s.listen()
            print(f"[SERVER] TCP Echo 서버 시작: {self.host}:{self.port}")

            while True:
                conn, addr = s.accept()
                handler = ClientHandler(conn, addr)
                handler.start()

if __name__ == "__main__":
    TCPServer().start()
