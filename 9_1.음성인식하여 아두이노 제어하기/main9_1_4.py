import speech_recognition as sr
import time
import serial
import serial.tools.list_ports

def send_rgb_led(red,green,blue):
    sendData = f"RGB={red},{green},{blue}\n"
    my_serial.write(sendData.encode())

def main():
    try:
        while True:
            r=sr.Recognizer()

            with sr.Microphone() as source:
                print("음성을 입력하세요.")
                audio = r.listen(source)
            try:
                stt = r.recognize_google(audio, language='ko-KR')
                print("음성변환: " + stt)
                if "빨간색" in stt and "켜" in stt:
                    print("빨간색 LED ON")
                    send_rgb_led(255,0,0)
                elif "녹색" in stt and "켜" in stt:
                    print("녹색 LED ON")
                    send_rgb_led(0,255,0)
                elif "파란색" in stt and "켜" in stt:
                    print("파란색 LED ON")
                    send_rgb_led(0,0,255)
                elif "불" in stt and "꺼" in stt:
                    print("모든 LED OFF")
                    send_rgb_led(0,0,0)
            
            except sr.UnknownValueError:
                print("오디오를 이해할 수 없습니다.")
            except sr.RequestError as e:
                print(f"에러가 발생하였습니다. 에러원인 : {e}")
    except KeyboardInterrupt:
        pass
    
if __name__=='__main__':
    ports = list(serial.tools.list_ports.comports())
    for p in ports:
        if 'Arduino Uno' in p.description:
            print(f"{p} 포트에 연결하였습니다.")
            my_serial = serial.Serial(p.device, baudrate=9600, timeout=1.0)
            time.sleep(2.0)
    main()

    my_serial.close()