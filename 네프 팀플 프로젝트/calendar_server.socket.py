import socket
import json
import pymysql

# -------------------------
# MySQL Connect
# -------------------------
def get_conn():
    return pymysql.connect(
        host='localhost',
        user='root',
        password='1234',
        db='calendar',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )

# -------------------------
# Request 처리 함수
# -------------------------
def handle_request(req):
    action = req.get("action")

    # -------------------------
    # 1) 회원가입
    # -------------------------
    if action == "register":
        email = req['email']
        pw = req['pw']
        name = req['name']

        conn = get_conn()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM Users WHERE email=%s", (email,))
        if cursor.fetchone():
            return {"success": False, "message": "이미 존재하는 이메일"}

        cursor.execute(
            "INSERT INTO Users(email, pw, name) VALUES (%s, %s, %s)",
            (email, pw, name),
        )
        conn.commit()
        return {"success": True, "message": "회원가입 완료"}

    # -------------------------
    # 2) 로그인
    # -------------------------
    if action == "login":
        email = req['email']
        pw = req['pw']

        conn = get_conn()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id FROM Users WHERE email=%s AND pw=%s",
            (email, pw)
        )
        row = cursor.fetchone()
        if row:
            return {"success": True, "user_id": row["id"]}
        else:
            return {"success": False, "message": "로그인 실패"}

    # -------------------------
    # 기본 응답
    # -------------------------
    return {"success": False, "message": "알 수 없는 action"}

# -------------------------
# TCP 서버 시작
# -------------------------
HOST = ''   # 모든 IP 허용
PORT = 5000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(5)

print(f"[Server] Python Socket 서버 실행 중... PORT={PORT}")

while True:
    conn, addr = server.accept()
    print(f"[클라이언트 접속] {addr}")

    data = conn.recv(4096).decode()
    print("[수신]", data)

    try:
        req_json = json.loads(data)
    except:
        conn.send(json.dumps({"success": False, "message": "JSON 파싱 실패"}).encode())
        conn.close()
        continue

    res = handle_request(req_json)

    conn.send(json.dumps(res).encode())
    conn.close()
