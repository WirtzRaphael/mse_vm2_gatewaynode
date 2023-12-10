import db.sqlite
import db.db
import radio.packages
import rc232.testing
import rc232.config
import rc232.serial
import rc232.radio
import schedule 
from schedule import every, repeat
import serial
import timeutil.timer

SERIAL_PORT_RC_DEVBOAD = '/dev/ttyUSB1'
DB_FILEPATH = r"gateway.db"

""" Initialzation
"""
def init_serial(serial_port: str, baud_rate: int = 19200, timeout: int = 1):
    serial_object = rc232.serial.serial_init(serial_port, baud_rate, timeout)
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

def init_db(db_file):
    db.sqlite.create_connection_test(db_file)
    db_connection = db.sqlite.create_connection(db_file)
    if db_connection is not None:
        db.sqlite.create_table(connection = db_connection,
                               create_table_sql = db.db.sql_create_temperature_1_table)
        db.sqlite.close_connection(db_connection)
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
        received_stream = rc232.radio.radio_receive(serial_object)
        print(received_stream)
        received_packages = radio.packages.split_into_packages(received_stream)
        if received_packages != None:
            db_connection = db.sqlite.create_connection(db_file = r"gateway.db")
            for package in received_packages:
                received_payload = radio.packages.payload_readout(package)
                if received_payload != None:
                    if received_payload.sensor_nr == '1':
                        db.db.insert_temperature_into_temperature1(connection = db_connection,
                                                temperature = (
                                                    received_payload.timestampRtc,
                                                    received_payload.sensorTemperatureValues[1].temperatureId,
                                                    received_payload.sensorTemperatureValues[1].temperature
                                                    ))
                    pass
            db.sqlite.close_connection(db_connection)
            # todo : write to db
    except serial.SerialException as e:
        print(f"Serial communication error: {e}")
    return None 

class mode_gateway_pc:
    def __init__(self):
        self.timer_repeated = None
        self.serial_rc = None

    def __enter__(self, *args, **kwargs):
        print("RUN pc mode \n")
        # initalization
        serial_rc = init_serial(serial_port= SERIAL_PORT_RC_DEVBOAD)
        init_db(DB_FILEPATH)
        # scheduling
        self.timer_repeated = timeutil.timer.RepeatedTimer(1, radio_read, serial_rc) # auto-starts
        schedule.every().day.at("00:00").do(time_sync)

    def __exit__(self, *args):
        print("EXIT pc mode")
        deinit_serial(self.serial_rc)
        self.timer_repeated.stop()
