# server_combined.py
import struct

HEADER_FMT = "!ii"  
HEADER_SIZE = struct.calcsize(HEADER_FMT)

def pack_frame(n: int, msg: str) -> bytes:
    data = msg.encode("utf-8")
    return struct.pack(HEADER_FMT, n, len(data)) + data

def recv_exact(sock, nbytes: int) -> bytes:
    buf = b""
    while len(buf) < nbytes:
        chunk = sock.recv(nbytes - len(buf))
        if not chunk:
            raise ConnectionError("Socket closed")
        buf += chunk
    return buf

def recv_frame(sock):
    header = recv_exact(sock, HEADER_SIZE)
    n, length = struct.unpack(HEADER_FMT, header)
    data = recv_exact(sock, length)
    return n, data.decode("utf-8")

import socket, threading

class ClientHandler(threading.Thread):
    def __init__(self, conn, addr):
        super().__init__(daemon=True)
        self.conn = conn
        self.addr = addr

    def run(self):
        try:
            n, msg = recv_frame(self.conn)
            for _ in range(n):
                self.conn.sendall(pack_frame(n, msg))
        except Exception as e:
            print(f"[ERROR] {self.addr}: {e}")
        finally:
            self.conn.close()

class EchoServer:
    def __init__(self, host="0.0.0.0", port=25000, backlog=100):
        self.host, self.port, self.backlog = host, port, backlog

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
    EchoServer().start()