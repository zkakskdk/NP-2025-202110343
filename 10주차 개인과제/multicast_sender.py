# multicast_sender.py
import socket
import struct
import time

MCAST_GRP = "224.1.1.1"
MCAST_PORT = 5000
INTERVAL = 2  
TTL = 1      

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, TTL)

    i = 1
    print(f"[SENDER] Multicast {MCAST_GRP}:{MCAST_PORT}, every {INTERVAL}s, TTL={TTL}")
    try:
        while True:
            msg = f"Multicast Message #{i}"
            sock.sendto(msg.encode(), (MCAST_GRP, MCAST_PORT))
            print("[송신]", msg)
            i += 1
            time.sleep(INTERVAL)
    except KeyboardInterrupt:
        print("\n[종료] 사용자 중단")
    finally:
        sock.close()

if __name__ == "__main__":
    main()
