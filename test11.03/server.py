# server.py
import socket, threading
from protocol import pack_frame, recv_frame

class ClientHandler(threading.Thread):
    def __init__(self, conn, addr):
        super().__init__(daemon=True)
        self.conn = conn
        self.addr = addr

    def run(self):
        try:
            n, msg = recv_frame(self.conn)
            # N번 동일 프레임 전송
            for _ in range(n):
                self.conn.sendall(pack_frame(n, msg))
        except Exception as e:
            # 로깅 간단화
            print(f"[ERROR] {self.addr}: {e}")
        finally:
            self.conn.close()

class EchoServer:
    def __init__(self, host="0.0.0.0", port=25000, backlog=100):
        self.host = host
        self.port = port
        self.backlog = backlog

    def start(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((self.host, self.port))
            s.listen(self.backlog)
            print(f"[N-ECHO] listening on {self.host}:{self.port}")
            while True:
                conn, addr = s.accept()
                print(f"[N-ECHO] client {addr} connected")
                ClientHandler(conn, addr).start()

if __name__ == "__main__":
    # 예: Ubuntu에서 서버
    EchoServer(port=25000).start()
