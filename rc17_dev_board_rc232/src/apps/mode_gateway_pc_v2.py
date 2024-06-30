import database.sqlite
import database.db_operation
import hdlc.hdlc
#import radio.packages
import rc232.testing
import rc232.config
import rc232.serial
import radio.radio
import schedule 
from schedule import every, repeat
#import re
import serial
import timeutil.timer
from sys import exit as sys_exit
from sys import stderr
import time


# todo : duplication
SERIAL_PORT = '/dev/ttyUSB0'
SERIAL_BAUDRATE = 19200
SERIAL_TIMEOUT = 0

DB_FILEPATH = r"gateway_v2.db"

""" Initialization serial
"""
def init_serial(serial_port: str, baud_rate: int = 19200, timeout: int = 1):
    serial_object = rc232.serial.serial_init(serial_port, baud_rate, timeout)
    try:
        if(serial_object.isOpen()):
            serial_object.close()
        serial_object.open()
    except serial.SerialException as e:
        print(f"Serial communication error: {e}")
    return serial_object

""" DEinitialization serial
"""
def deinit_serial(serial_object: serial.Serial):
    try:
        serial_object.close()
    except serial.SerialException as e:
        print(f"Serial communication error: {e}")
    return None

""" Initialization database
"""
def init_db(db_file):
    with database.sqlite.DbConnection(db_file) as db_connection:
        if db_connection is not None:
            database.sqlite.create_table(connection = db_connection,
                                        create_table_sql = database.db_operation.SQL_CREATE_SENSORNODES_TABLE)
            database.sqlite.create_table(connection = db_connection,
                                        create_table_sql = database.db_operation.SQL_CREATE_SENSORNODES_SENSORS_TABLE)
            database.sqlite.create_table(connection = db_connection,
                                        create_table_sql = database.db_operation.SQL_CREATE_SENSORNODES_MEASUREMENTS_TABLE)
    return None

""" Functions
"""
def run_mode_gateway_pc_v2(operation_mode, rc_usb_port:serial, rc_usb_used:bool):
    print("RUN pc mode \n")
    #self.timer_repeated = None
    #self.serial_rc = None
    # initalization
    if(rc_usb_used):
        serial_rc = init_serial(serial_port= rc_usb_port)
    else:  
        print("No serial port")
    init_db(DB_FILEPATH)
    #with(database.sqlite.DbConnection(DB_FILEPATH)) as db_connection:
    #    insert_temperatures_testdata_into_database
    
    # scheduling
    #self.timer_repeated = timeutil.timer.RepeatedTimer(1,radio_read, serial_rc) # auto-starts
    #schedule.every(1).seconds.do(radio_read, serial_rc) # sometimes conflict with serial port
    #schedule.every(1).seconds.do(radio_read_hdlc()) # sometimes conflict with serial port
    #schedule.every().day.at("00:00").do(time_sync)
    
    while(operation_mode == 'gateway_pc_v2'):
        #schedule.run_pending()

        # todo : error handling
        #radio.radio.radio_receive_write_to_file(serial_rc)
        # RECEIVE
        binary_data = radio.radio.read_received_data_from_file()
        hdlc_frames = hdlc.hdlc.hdlc_decode(binary_data)

        for i, frame in enumerate(hdlc_frames):
            print(f"Frame {i + 1}: {frame.hex()}")
            
        # DECODE

        #radio_read_hdlc()
        #radio_read(serial_rc)

        #plot_measurements()
        time.sleep(1)
        

    print("EXIT pc mode")
    #deinit_serial(self.serial_rc)
    #self.timer_repeated.stop()
    
    #radio_read(self.serial_rc)
    return


# todo : for v2
def insert_temperatures_into_database(db_connection:database.sqlite.DbConnection):
    print("db  operation")
    for sensorTemperature in payload.sensorTemperatureValues:
        # todo : limit unix time after coma
        time_received_unix_s = timeutil.timeutil.get_time_unix_s()
        sensor_timestamp_rtc = payload.timestampRtc + sensorTemperature.time_relative_to_reference
        sensor_id = payload.sensor_nr
        database.db_operation.insert_temperature_into_sensor_data(connection = db_connection,
                                                    sensor_data = (
                                                        time_received_unix_s,
                                                        sensor_timestamp_rtc,
                                                        sensorTemperature.temperatureId,
                                                        10,
                                                        sensor_id,
                                                        sensorTemperature.temperature, 
                                                        signal_strength))
    return None

def insert_temperatures_testdata_into_database(db_connection:database.sqlite.DbConnection):
    database.db_operation.insert_temperature_into_measurements(connection = db_connection, measurements = (10, 1234567890, 1, 25.0))
    database.db_operation.insert_temperature_into_measurements(connection = db_connection, measurements = (10, 1234567895, 1, 24.5))
    database.db_operation.insert_temperature_into_measurements(connection = db_connection, measurements = (10, 1234567900, 1, 24.0))
    database.db_operation.insert_temperature_into_measurements(connection = db_connection, measurements = (10, 1234567905, 1, 24.5))
    return None
