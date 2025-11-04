import socket
import threading

class NEchoServer:
    def __init__(self, host="0.0.0.0", port=2500, backlog=100):
        self.host = host
        self.port = port
        self.backlog = backlog

    def start(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as srv:
            srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            srv.bind((self.host, self.port))
            srv.listen(self.backlog)
            print(f"[N-ECHO(Simple)] listening on {self.host}:{self.port}")
            while True:
                conn, addr = srv.accept()
                print(f"[N-ECHO(Simple)] client {addr} connected")
                threading.Thread(target=self.handle_client, args=(conn, addr), daemon=True).start()

    def handle_client(self, conn: socket.socket, addr):
        try:
            # 간단 클라이언트는 한 번에 "n msg"를 보냄
            raw = conn.recv(4096)
            if not raw:
                return

            text = raw.decode("utf-8", errors="ignore").strip()
            # "n msg" 형태에서 첫 공백 기준으로 분리
            if " " not in text:
                conn.sendall("[서버 오류] 형식은 'n msg' 입니다.".encode("utf-8"))
                return

            n_str, msg = text.split(" ", 1)
            try:
                n = int(n_str)
            except ValueError:
                conn.sendall("[서버 오류] n은 정수여야 합니다.".encode("utf-8"))
                return

            if n < 1:
                conn.sendall("[서버 오류] n은 1 이상이어야 합니다.".encode("utf-8"))
                return

            # 클라이언트는 응답을 '한 번만' recv(1024) 하므로
            # 한 번에 몰아서 보내준다. (줄바꿈으로 N개 붙이기)
            repeated = ("\n".join([msg] * n)).encode("utf-8")
            conn.sendall(repeated)

        except Exception as e:
            print(f"[ERROR] {addr}: {e}")
        finally:
            conn.close()

if __name__ == "__main__":
    NEchoServer(port=2500).start()
