import serial
import time
import rc232.rc232_testing
import rc232.rc232_config
import rc232.rc232_serial
import rc232.rc232_radio
import measurments.rc_send
import radio.packages
import timeutil.timer
import timeutil.timeutil
import threading 
import schedule 
from schedule import every, repeat

""" Variables
"""
serial_port = '/dev/ttyUSB0'
baud_rate = 19200 
timeout = 1

operation_mode = {
    'production',
    'debug'
    'testing'
}


""" Functions
"""
@repeat(every(20).seconds, message = "write")
@repeat(every(100).seconds, message = "check")
def database_operation(message):
    print("Database: ", message, "\n")
    # implement
    return

def time_sync():
    print("time_sync \n")
    # implement
    return

def radio_read(serial_object: serial.Serial):
    print("thread_sensor")
    try:
        received_package = rc232.rc232_radio.radio_receive(serial_object)
        received_package_deserialized = radio.packages.deserialization_sensor(received_package)
        print("received_package_deserialized: ", received_package_deserialized)
    except serial.SerialException as e:
        print(f"Serial communication error: {e}")
    


""" Initialzation
"""
def init_serial():
    dev_board_serial_20 = rc232.rc232_serial.SerialRcDevBoard(serial_port, baud_rate, timeout)
    dev_board_config_20 = rc232.rc232_config.RC232Configuration(channel=1, destination_id=20, power=0, rssi_mode=1, unique_id=10)
    serial_20 = rc232.rc232_serial.serial_init(dev_board_serial_20.port, dev_board_serial_20.baud_rate, dev_board_serial_20.timeout)
    try:
        serial_20.open()
    except serial.SerialException as e:
        print(f"Serial communication error: {e}")
    return serial_20


operation_mode = 'production'

class ModeProduction:
    def __init(self):
        self.timer_repeated = None

    def __enter__(self, *args, **kwargs):
        print("RUN production mode \n")
        # init
        serial = init_serial()

        # scheduling
        self.timer_repeated = timeutil.timer.RepeatedTimer(1, radio_read, serial) # auto-starts
        schedule.every().day.at("00:00").do(time_sync)

    def __exit__(self, *args):
        print("--EXIT production mode--")
        self.timer_repeated.stop()


def run_mode_production():
    return

def run_mode_debug():
    return

def run_mode_testing():
    measurments.rc_send.rc_send(serial_20, dev_board_config_20)
    return

while(True):
    match operation_mode:
        case 'production':
            with ModeProduction():
                while(operation_mode == 'production'):
                    run_mode_production()
        case 'debug':
            print("debug \n")
            run_mode_debug()
        case 'testing':
            print("testing \n")
            run_mode_testing()
        case _:
            print("no mode\n")
    time.sleep(0.5)



# Deinitialization
try:
    serial_10.close()
except serial.SerialException as e:
    print(f"Serial communication error: {e}")

