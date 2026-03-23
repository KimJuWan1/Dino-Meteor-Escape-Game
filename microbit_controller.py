# microbit_controller.py
import serial
import threading

# COM 포트 설정 (자신 환경에 맞게 수정)
PORT = 'COM3'
BAUDRATE = 115200

# 공유 변수
tilt_x = 0
tilt_y = 0
tilt_z = 0
button_a = False
button_b = False
microbit_thread_running = True

def read_microbit():
    global tilt_x, tilt_y, tilt_z, button_a, button_b, microbit_thread_running
    try:
        with serial.Serial(PORT, BAUDRATE, timeout=1) as ser:
            print(f"[INFO] Microbit 연결됨: {PORT}")
            while microbit_thread_running:
                line = ser.readline().decode().strip()
                if line:
                    parts = line.split(',')
                    if len(parts) == 5:
                        try:
                            tilt_x = int(parts[0])
                            tilt_y = int(parts[1])
                            tilt_z = int(parts[2])
                            button_a = bool(int(parts[3]))
                            button_b = bool(int(parts[4]))
                        except ValueError:
                            print("[WARN] 변환 오류:", parts)
                            continue

    except serial.SerialException as e:
        print(f"[Microbit Serial Error] {e}")

# 백그라운드에서 마이크로비트 읽기 시작
def start_microbit_thread():
    thread = threading.Thread(target=read_microbit, daemon=True)
    thread.start()

# 게임 루프에서 사용
def get_microbit_tilt():
    return tilt_x, tilt_y

def is_button_a_pressed():
    return button_a

def is_button_b_pressed():
    return button_b

def stop_microbit_thread():
    global microbit_thread_running
    microbit_thread_running = False
