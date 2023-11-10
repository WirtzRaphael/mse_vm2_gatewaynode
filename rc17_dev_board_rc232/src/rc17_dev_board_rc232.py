import difflib
import pickle
import serial
import time
import rc232
import rc_serial
import rc_measurements
import rc_send_receive
#import rc_receive
import measurments.rc_send


baud_rate = 19200 
class SerialRcDevBoard:
    def __init__(self, port, baud_rate):
        self.port = port
        self.baud_rate = baud_rate
dev_board_serial_10 = SerialRcDevBoard('/dev/ttyUSB0', baud_rate)
dev_board_config_10 = rc232.RC232Configuration(channel=1, destination_id=20, power=0, rssi_mode=1, unique_id=10)
serial_10 = rc_serial.serial_init(dev_board_serial_10.port, dev_board_serial_10.baud_rate)

try:
    serial_10.open()
except serial.SerialException as e:
    print(f"Serial communication error: {e}")

#rc_receive.rc_receive()
measurments.rc_send.rc_send(serial_10, dev_board_config_10)

try:
    serial_10.close()
except serial.SerialException as e:
    print(f"Serial communication error: {e}")

print("End of program.")
