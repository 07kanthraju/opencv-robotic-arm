import serial
import time

class ServoController:
    def __init__(self, port="/dev/ttyUSB0", baud_rate=9600, delay=0.3):
        self.delay = delay
        try:
            self.ser = serial.Serial(port, baud_rate, timeout=1)
            time.sleep(2)
            print(f"Connected to Arduino at {port}")
        except Exception as e:
            print(f"Could not connect to Arduino: {e}")
            self.ser = None

    def send_command(self, ch, angle):
        if not self.ser:
            print("Arduino not connected.")
            return
        cmd = f"S,{ch},{angle}\n"
        self.ser.write(cmd.encode())
        print(f"➡ Sent: {cmd.strip()}")
        time.sleep(self.delay)

    def close(self):
        if self.ser:
            self.ser.close()
