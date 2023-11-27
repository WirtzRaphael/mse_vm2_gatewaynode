import serial
import time
import rc232.rc232
import rc232.rc232_config
import rc232.rc_serial
import measurments.rc_send

serial_port = '/dev/ttyUSB0'
baud_rate = 19200 
timeout = 1

class SerialRcDevBoard:
    def __init__(self, port, baud_rate, timeout):
        self.port = port
        self.baud_rate = baud_rate
        self.timeout = timeout


dev_board_serial_10 = SerialRcDevBoard(serial_port, baud_rate, timeout)
dev_board_config_10 = rc232.rc232_config.RC232Configuration(channel=1, destination_id=20, power=0, rssi_mode=1, unique_id=10)
serial_10 = rc232.rc_serial.serial_init(dev_board_serial_10.port, dev_board_serial_10.baud_rate, dev_board_serial_10.timeout)
try:
    serial_10.open()
except serial.SerialException as e:
    print(f"Serial communication error: {e}")


voltage = rc232.rc232_config.read_voltage(serial_10, dryrun=False)
memory = rc232.rc232_config.read_memory_one_byte(serial_10, dryrun=False)
print(f"memory: {memory}")
rc232.rc232_config.set_rf_power(serial_10,1)
memory = rc232.rc232_config.read_memory_one_byte(serial_10, dryrun=True)
print(f"memory: {memory}")

temperature_1 = rc232.rc232_config.read_temperature(serial_10, dryrun=False)
print(f"temperature_1: {temperature_1}")
print(f"voltage: {voltage}")
temperature_2 = rc232.rc232_config.read_temperature(serial_10, dryrun=False)
print(f"temperature_2: {temperature_2}")


#measurments.rc_send.rc_send(serial_10, dev_board_config_10)

try:
    serial_10.close()
except serial.SerialException as e:
    print(f"Serial communication error: {e}")

