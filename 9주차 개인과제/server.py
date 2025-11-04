import socket
import threading
import datetime

HOST = "0.0.0.0" 
TIME_PORT = 5001
ECHO_PORT = 5002
NUMBER_PORT = 5003
ENC = "utf-8"
BUF = 4096


def handle_time(conn, addr):
    try:
        _ = conn.recv(BUF)
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        conn.sendall(f"TIME {now}\n".encode(ENC))
    except Exception as e:
        conn.sendall(f"ERR {e}\n".encode(ENC))
    finally:
        conn.close()
def handle_echo(conn, addr):
    try:
        conn.sendall("echo 서버입니다. 'quit'입력 시 나가기.\n".encode(ENC))
        while True:
            data = conn.recv(BUF)
            if not data:
                break
            text = data.decode(ENC).strip()
            if text.lower() == "quit":
                conn.sendall("bye\n".encode(ENC))
                break
            conn.sendall((text + "\n").encode(ENC))
    except Exception as e:
        conn.sendall(f"ERR {e}\n".encode(ENC))
    finally:
        conn.close()


def handle_number(conn, addr):
    try:
        conn.sendall("결과:\n".encode(ENC))
        data = conn.recv(BUF)
        if not data:
            return
        text = data.decode(ENC).strip()
        if not text.isdigit():
            conn.sendall("ERR N must be a number.\n".encode(ENC))
            return
        n = int(text)
        if n < 1 or n > 100000:
            conn.sendall("ERR N must be within 1~100000.\n".encode(ENC))
            return
        numbers = " ".join(str(i) for i in range(1, n + 1))
        conn.sendall((numbers + "\n").encode(ENC))
    except Exception as e:
        conn.sendall(f"ERR {e}\n".encode(ENC))
    finally:
        conn.close()


def serve(port, handler):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, port))
    s.listen()
    print(f"[LISTEN] {handler.__name__} on port {port}")
    while True:
        conn, addr = s.accept()
        threading.Thread(target=handler, args=(conn, addr), daemon=True).start()


def main():
    threading.Thread(target=serve, args=(TIME_PORT, handle_time), daemon=True).start()
    threading.Thread(target=serve, args=(ECHO_PORT, handle_echo), daemon=True).start()
    threading.Thread(target=serve, args=(NUMBER_PORT, handle_number), daemon=True).start()
    print("Servers are running... Press Ctrl+C to stop.")
    try:
        while True:
            threading.Event().wait(3600)
    except KeyboardInterrupt:
        print("Shutting down...")


if __name__ == "__main__":
    main()