# client_combined.py
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

import socket, sys

class EchoClient:
    def __init__(self, host="127.0.0.1", port=25000):
        self.host, self.port = host, port

    def run(self, n: int, msg: str):
        with socket.create_connection((self.host, self.port)) as s:
            s.sendall(pack_frame(n, msg))
            for i in range(1, n+1):
                n_resp, msg_resp = recv_frame(s)
                print(f"[{i}/{n_resp}] {msg_resp}")

if __name__ == "__main__":
    host = sys.argv[1] if len(sys.argv) > 1 else "127.0.0.1"
    port = int(sys.argv[2]) if len(sys.argv) > 2 else 25000
    n    = int(sys.argv[3]) if len(sys.argv) > 3 else 3
    msg  = sys.argv[4] if len(sys.argv) > 4 else "hello"
    EchoClient(host, port).run(n, msg)
