import db.sqlite
import radio.packages
import rc232.testing
import rc232.config
import rc232.serial
import rc232.radio
import schedule 
from schedule import every, repeat
import serial
import timeutil.timer


""" Initialzation
"""
def init_serial(serial_port: str, baud_rate: int = 19200, timeout: int = 1):
    serial_object = rc232.rc232_serial.serial_init(serial_port, baud_rate, timeout)
    try:
        serial_object.open()
    except serial.SerialException as e:
        print(f"Serial communication error: {e}")
    return serial_object

def deinit_serial(serial_object: serial.Serial):
    try:
        serial_object.close()
    except serial.SerialException as e:
        print(f"Serial communication error: {e}")
    return None


""" Functions
"""
def run_mode_gateway_pc():
   return

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
        # todo : write to db
    except serial.SerialException as e:
        print(f"Serial communication error: {e}")


class mode_gateway_pc:
    def __init__(self):
        self.timer_repeated = None
        self.serial_rc = None

    def __enter__(self, *args, **kwargs):
        print("RUN pc mode \n")
        # init
        serial_rc = init_serial(serial_port= '/dev/ttyUSB2')
        # scheduling
        self.timer_repeated = timeutil.timer.RepeatedTimer(1, radio_read, serial_rc) # auto-starts
        schedule.every().day.at("00:00").do(time_sync)

    def __exit__(self, *args):
        print("EXIT pc mode")
        deinit_serial(serial_rc)
        self.timer_repeated.stop()
