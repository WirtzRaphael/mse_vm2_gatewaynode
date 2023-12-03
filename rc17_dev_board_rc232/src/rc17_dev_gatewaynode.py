import serial
import time
import rc232.rc232_testing
import rc232.rc232_config
import rc232.rc232_serial
import rc232.rc232_radio
import measurments.rc_send

serial_port = '/dev/ttyUSB0'
baud_rate = 19200 
timeout = 1


# Initialization
dev_board_serial_20 = rc232.rc232_serial.SerialRcDevBoard(serial_port, baud_rate, timeout)
dev_board_config_20 = rc232.rc232_config.RC232Configuration(channel=1, destination_id=20, power=0, rssi_mode=1, unique_id=10)
serial_20 = rc232.rc232_serial.serial_init(dev_board_serial_20.port, dev_board_serial_20.baud_rate, dev_board_serial_20.timeout)
try:
    serial_20.open()
except serial.SerialException as e:
    print(f"Serial communication error: {e}")

while(True):
    #radioConfigRead()
    rc232.rc232_radio.radio_receive(serial_20)
    time.sleep(0.5)
    


#measurments.rc_send.rc_send(serial_10, dev_board_config_10)

# Deinitialization
try:
    serial_10.close()
except serial.SerialException as e:
    print(f"Serial communication error: {e}")

