import serial
import time
import rc232.rc232
import rc232.rc_serial
import measurments.rc_receive
import measurments.rc_send

action = "send"
#action = "receive"
serial_port = '/dev/ttyUSB0'
#serial_port = '/dev/ttyUSB1'

baud_rate = 19200 
class SerialRcDevBoard:
    def __init__(self, port, baud_rate):
        self.port = port
        self.baud_rate = baud_rate

if (action == "send"):
    dev_board_serial_10 = SerialRcDevBoard(serial_port, baud_rate)
    dev_board_config_10 = rc232.rc232.RC232Configuration(channel=1, destination_id=20, power=0, rssi_mode=1, unique_id=10)
    serial_10 = rc232.rc_serial.serial_init(dev_board_serial_10.port, dev_board_serial_10.baud_rate)
    try:
        serial_10.open()
    except serial.SerialException as e:
        print(f"Serial communication error: {e}")


if (action == "receive"):
    dev_board_serial_20 = SerialRcDevBoard('/dev/ttyUSB0', baud_rate)
    dev_board_config_20 = rc232.rc232.RC232Configuration(channel=1, destination_id=10, power=0, rssi_mode=1, unique_id=20)
    serial_20 = rc232.rc_serial.serial_init(dev_board_serial_20.port, dev_board_serial_20.baud_rate)
    try:
        serial_20.open()
    except serial.SerialException as e:
        print(f"Serial communication error: {e}")


if (action == "send"):
    measurments.rc_send.rc_send(serial_10, dev_board_config_10)
if (action == "receive"):
    measurments.rc_receive.rc_receive(serial_20, dev_board_config_20)


if (action == "send"):
    try:
        serial_10.close()
    except serial.SerialException as e:
        print(f"Serial communication error: {e}")

if (action == "receive"):
    try:
        serial_20.close()
    except serial.SerialException as e:
        print(f"Serial communication error: {e}")

print("End of program.")
