import time
import serial
import serial.tools.list_ports
import threading

def send_servo(digree):
    sendData = f"SERVO={digree}\n"
    my_serial.write(sendData.encode())
def send_buzzer(freq):
    sendData = f"BUZZER={freq}\n"
    my_serial.write(sendData.encode())
def send_fnd(data):
    sendData = f"FND={data}\n"
    my_serial.write(sendData.encode())
def serial_read_thread():
    while True:
        read_data = my_serial.readline()
        print(read_data.decode())
def main():
    try:
        while True:
            send_servo(0)
            send_buzzer(261)
            send_fnd(1234)
            time.sleep(1.0)

            send_servo(90)
            send_buzzer(293)
            send_fnd(5678)
            time.sleep(1.0)

            send_servo(180)
            send_buzzer(329)
            send_fnd(3.14)
            time.sleep(1.0)

            send_servo(90)
            send_buzzer(349)
            send_fnd(12.34)
            time.sleep(1.0)
    except KeyboardInterrupt:
        send_buzzer(0)
if __name__ == "__main__":
    ports = list(serial.tools.list_ports.comports())
    for p in ports:
        if 'Arduino Uno' in p.description:
            print(f"{p} 포트에 연결하였습니다.")
            my_serial = serial.Serial(p.device, baudrate=9600, timeout=1.0)
            time.sleep(2.0)

    t1 = threading.Thread(target=serial_read_thread)
    t1.daemon = True
    t1.start()

    main()

    my_serial.close()