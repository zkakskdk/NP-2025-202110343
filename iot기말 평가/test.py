import requests
import time
import serial
import serial.tools.list_ports
from datetime import datetime

# ---------------------------
# 0) 기상청 오픈API 기본 설정
# ---------------------------
SERVICE_KEY = "95645910ce53ff082f5070a82b7c8aa404e6a0f11f88c9b15e6ee51625c67b45"
END_POINT = "https://apis.data.go.kr/1360000/VilageFcstInfoService_2.0"

# ---------------------------
# 1) RGB 데이터 전송 함수
# ---------------------------
def send_rgb_led(red, green, blue):
    sendData = f"RGB={red},{green},{blue}\n"
    my_serial.write(sendData.encode())

# ---------------------------
# 2) 아두이노 포트 찾기
# ---------------------------
def find_arduino():
    ports = list(serial.tools.list_ports.comports())
    for p in ports:
        if 'Arduino' in p.description or 'Uno' in p.description:
            print(f"{p.device} 포트에 연결됨!")
            return serial.Serial(p.device, baudrate=9600, timeout=1.0)

    raise Exception("⚠ Arduino 포트를 찾지 못했습니다.")

# ---------------------------
# 3) 기상청 오픈API에서 강수확률 가져오기
# ---------------------------
def get_rain_prob_from_api():
    # 오늘 날짜 (예: 20251211)
    base_date = datetime.now().strftime("%Y%m%d")
    # 예보 기준 시간 (대충 아침 05시, 08시 등 중 하나 선택)
    base_time = "0800"

    # 예시로 서울 (nx=60, ny=127) 사용
    nx = 56
    ny = 38

    url = f"{END_POINT}/getVilageFcst"

    params = {
        "serviceKey": SERVICE_KEY,  # 일반 인증키
        "pageNo": 1,
        "numOfRows": 1000,
        "dataType": "JSON",
        "base_date": base_date,
        "base_time": base_time,
        "nx": nx,
        "ny": ny,
    }

    try:
        res = requests.get(url, params=params)
        res.raise_for_status()  # HTTP 오류 나면 예외 발생
        data = res.json()

        items = data["response"]["body"]["items"]["item"]

        # 카테고리 'POP' = 강수확률
        # 여러 시간대가 있을 수 있으니 일단 첫 번째 POP 사용
        for item in items:
            if item["category"] == "POP":
                rain_prob = int(item["fcstValue"])
                fcst_time = item["fcstTime"]
                print(f"예보시간 {fcst_time} 기준 강수확률: {rain_prob}%")
                return rain_prob

        # 여기까지 왔다는 건 POP를 못 찾았다는 뜻
        raise ValueError("POP(강수확률) 데이터를 찾지 못했습니다.")

    except Exception as e:
        print("⚠ 오픈API 호출 실패:", e)
        print("일단 기본값 0으로 처리할게요.")
        return 0

# ---------------------------
# 4) 메인 로직
# ---------------------------
def main():
    # 🔁 이전에는 CSV에서 읽어왔던 부분
    # df = pd.read_csv("rain_data.csv", encoding="utf-8")
    # today = "2025-12-11"
    # row = df[df["date"] == today]
    # rain_prob = int(row["rain_prob"].values[0])

    rain_prob = get_rain_prob_from_api()  # ← 이 한 줄이 API 연동 핵심

    print("오늘 강수확률:", rain_prob)

    if rain_prob >= 60:
        print("우산 챙기세요! -> 빨간색 표시")
        send_rgb_led(255, 0, 0)
    else:
        print("오늘은 괜찮습니다 -> 파란색 표시")
        send_rgb_led(0, 0, 255)

# ---------------------------
# 5) 실행부
# ---------------------------
if __name__ == "__main__":
    my_serial = find_arduino()
    time.sleep(2)  # 아두이노 초기화 대기
    main()
    my_serial.close()
