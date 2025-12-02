import socket
import threading
import datetime

HOST = "0.0.0.0" 
PORT = 2500      

def process_request(line: str) -> str:

    parts = line.strip().split()

    if not parts:
        return "ERROR: empty request"

    cmd = parts[0].upper()


    if cmd == "TIME":
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return f"TIME: {now}"


    if cmd == "QUIT":
        return "BYE"

    if cmd in ("ADD", "SUB", "MUL", "DIV"):
        if len(parts) != 3:
            return "ERROR: usage -> ADD a b / SUB a b / MUL a b / DIV a b"

        try:
            a = float(parts[1])
            b = float(parts[2])
        except ValueError:
            return "ERROR: arguments must be numbers"

        if cmd == "ADD":
            result = a + b
        elif cmd == "SUB":
            result = a - b
        elif cmd == "MUL":
            result = a * b
        elif cmd == "DIV":
            if b == 0:
                return "ERROR: division by zero"
            result = a / b

        return f"RESULT: {result}"

    return f"ERROR: unknown command '{cmd}'"


def handle_client(conn: socket.socket, addr):
    print(f"[INFO] 클라이언트 접속: {addr}")


    try:
        with conn, conn.makefile("r", encoding="utf-8") as rf:
            while True:
                line = rf.readline()
                if not line:  
                    print(f"[INFO] 클라이언트 종료: {addr}")
                    break

                line = line.strip()
                if not line:
                    continue

                print(f"[RECV from {addr}] {line}")

                if line.upper() == "QUIT":
                    # 종료 요청
                    response = "BYE"
                    conn.sendall((response + "\n").encode("utf-8"))
                    print(f"[INFO] QUIT 처리 후 연결 종료: {addr}")
                    break

                response = process_request(line)
                conn.sendall((response + "\n").encode("utf-8"))
    except Exception as e:
        print(f"[ERROR] {addr} 처리 중 예외 발생: {e}")


def main():
    print(f"[INFO] 서버 시작... {HOST}:{PORT}")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_sock:
        server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_sock.bind((HOST, PORT))
        server_sock.listen()

        print("[INFO] 클라이언트 접속 대기 중...")

        while True:
            conn, addr = server_sock.accept()
            t = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
            t.start()


if __name__ == "__main__":
    main()
