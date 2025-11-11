# receiver.py
import socket

PORT = 3000
BUF = 2048

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("", PORT))
    print(f"[RECEIVER] UDP 수신 대기중 : 0.0.0.0:{PORT}")

    try:
        while True:
            data, addr = sock.recvfrom(BUF)
            print(f"[수신] from {addr} : {data.decode(errors='ignore').strip()}")
    except KeyboardInterrupt:
        print("\n[종료] 사용자 중단")
    finally:
        sock.close()

if __name__ == "__main__":
    main()
