import time
import serial
import serial.tools.list_ports
import threading

def send_temperature():
    sendData = f"TEMPERATURE=?\n"
    my_serial.write(sendData.encode())
def send_humidity():
    sendData = f"HUMIDITY=?\n"
    my_serial.write(sendData.encode())
def send_object_temperature():
    sendData = f"OBJECT=?\n"
    my_serial.write(sendData.encode())


def serial_read_thread():
    global serial_receive_data
    while True:
        read_data = my_serial.readline()
        serial_receive_data = read_data.decode()
def send_vr_bright_1sec():
    t2 = threading.Timer(1,send_vr_bright_1sec)
    t2.daemon = True
    t2.start()
    send_temperature()
    time.sleep(0.2)
    send_humidity()
    time.sleep(0.2)
    send_object_temperature()
    time.sleep(0.2)
    # send_ambient_temperature()

def main():
    try:
        send_vr_bright_1sec()
        global serial_receive_data
        while True:
            if "TEMPERATURE=" in serial_receive_data:
                print("온도: ", serial_receive_data[12:])
                serial_receive_data = ""
            elif "HUMIDITY=" in serial_receive_data:
                print("습도: ", serial_receive_data[9:])
                serial_receive_data = ""
            elif "OBJECT=" in serial_receive_data:
                print("물체온도: ", serial_receive_data[7:])
                serial_receive_data = ""
            elif "AMBIENT=" in serial_receive_data:
                print("주변온도: ", serial_receive_data[8:])
                serial_receive_data = ""
    except KeyboardInterrupt:
        pass
if __name__ == '__main__':
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