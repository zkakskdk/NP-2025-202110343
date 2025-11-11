# multicast_receiver.py
import socket
import struct
import sys

MCAST_GRP = "224.1.1.1"
MCAST_PORT = 5000
BUF = 2048

LOCAL_IF = "0.0.0.0" 

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    sock.bind(("", MCAST_PORT))
    print(f"[RECEIVER] Bind: 0.0.0.0:{MCAST_PORT}, Join: {MCAST_GRP} (IF={LOCAL_IF})")

    mreq = struct.pack("=4s4s",
                       socket.inet_aton(MCAST_GRP),
                       socket.inet_aton(LOCAL_IF))
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    try:
        while True:
            data, addr = sock.recvfrom(BUF)
            print(f"[수신] from {addr} : {data.decode(errors='ignore').strip()}")
    except KeyboardInterrupt:
        print("\n[종료] 사용자 중단")
    finally:
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_DROP_MEMBERSHIP, mreq)
        sock.close()

if __name__ == "__main__":
    if len(sys.argv) >= 2:
        LOCAL_IF = sys.argv[1]
    main()
