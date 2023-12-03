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
        
class RadioConfigRead:
    def __init__(self):
        self.voltage = 0
        self.memory_power = 0
        self.memory_datarate = 0
        self.temperature = 0

def radioConfigRead(serial_object: serial.Serial, radio_config_read: RadioConfigRead):
    radio_config_read.voltage = rc232.rc232_config.read_voltage(serial_object, dryrun=False)
    radio_config_read.memory_power = rc232.rc232_config.read_memory_one_byte(serial_object, 0x01 ,dryrun=False)
    print(f"memory: {radio_config_read.memory_power}")
    #rc232.rc232_config.set_rf_power(serial_10,1)
    radio_config_read.memory_datarate = rc232.rc232_config.read_memory_one_byte(serial_object, 0x02, dryrun=False)
    print(f"memory: {radio_config_read.memory_datarate}")

    radio_config_read.temperature = rc232.rc232_config.read_temperature(serial_object, dryrun=False)
    print(f"temperature_1: {radio_config_read.temperature_1}")
    print(f"voltage: {radio_config_read.voltage}")

def radioReceive(serial_object: serial.Serial):
    try:
        # fix : package size, no magik number
        received_package_bin = serial_object.read(37)
        received_package = received_package_bin.decode()
        #file_rec.write(received_package)
        print(f"Received data: {received_package}")
    except serial.SerialException as e:
        print(f"Serial communication error: {e}")


# Initialization
radio_config_read = RadioConfigRead()

dev_board_serial_20 = SerialRcDevBoard(serial_port, baud_rate, timeout)
dev_board_config_20 = rc232.rc232_config.RC232Configuration(channel=1, destination_id=20, power=0, rssi_mode=1, unique_id=10)
serial_20 = rc232.rc_serial.serial_init(dev_board_serial_20.port, dev_board_serial_20.baud_rate, dev_board_serial_20.timeout)
try:
    serial_20.open()
except serial.SerialException as e:
    print(f"Serial communication error: {e}")

while(True):
    #radioConfigRead()
    radioReceive(serial_20)
    time.sleep(0.5)
    


#measurments.rc_send.rc_send(serial_10, dev_board_config_10)

# Deinitialization
try:
    serial_10.close()
except serial.SerialException as e:
    print(f"Serial communication error: {e}")

