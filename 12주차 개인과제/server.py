import socket
import threading

HOST = '0.0.0.0'
PORT = 2500

clients = []

def broadcast(message, sender_socket=None):
    for client in clients:
        if client != sender_socket:
            try:
                client.send(message)
            except:
                pass

def handle_client(client_socket, addr):
    print(f"[INFO] {addr} 클라이언트 연결됨")

    try:
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            print(f"[RECV from {addr}] {data.decode('utf-8', errors='ignore')}")
            broadcast(data, sender_socket=client_socket)
    except:
        pass
    finally:
        print(f"[INFO] {addr} 클라이언트 연결 종료")
        if client_socket in clients:
            clients.remove(client_socket)
        client_socket.close()

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server_socket.bind((HOST, PORT))
    server_socket.listen()
    print(f"[START] 채팅 서버 시작됨 - 포트 {PORT} 대기 중...")

    try:
        while True:
            client_socket, addr = server_socket.accept()
            clients.append(client_socket)
            thread = threading.Thread(target=handle_client, args=(client_socket, addr), daemon=True)
            thread.start()
    except KeyboardInterrupt:
        print("\n[STOP] 서버 종료")
    finally:
        for c in clients:
            c.close()
        server_socket.close()

if __name__ == "__main__":
    main()
