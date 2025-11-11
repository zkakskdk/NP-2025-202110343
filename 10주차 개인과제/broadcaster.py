# broadcaster.py
import socket
import time

PORT = 3000
INTERVAL = 2  

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    i = 1
    print(f"[BROADCASTER] <broadcast>:{PORT} 로 {INTERVAL}s 간격 송신 시작")
    try:
        while True:
            msg = f"Broadcast Test #{i}"
            sock.sendto(msg.encode(), ("<broadcast>", PORT))
            print(f"[송신] {msg}")
            i += 1
            time.sleep(INTERVAL)
    except KeyboardInterrupt:
        print("\n[종료] 사용자 중단")
    finally:
        sock.close()

if __name__ == "__main__":
    main()
