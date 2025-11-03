# protocol.py
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