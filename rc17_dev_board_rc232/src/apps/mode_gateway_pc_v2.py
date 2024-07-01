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
from datetime import datetime
from sys import exit as sys_exit
from sys import stderr
import time
import visualize.plot_database

# todo : duplication
SERIAL_PORT = '/dev/ttyUSB0'
SERIAL_BAUDRATE = 19200
SERIAL_TIMEOUT = 0

# todo : duplication
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

""" Deinitialization serial
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

        # todo : error handling, no data
        #radio.radio.radio_receive_write_to_file(serial_rc)
        # RECEIVE
        #binary_data = radio.radio.read_received_data_from_file()
        try :
            # READ
            print("Read data")
            data_bytearray = radio.radio.radio_read(serial_rc)

            if data_bytearray is None:
                continue

            #radio.radio.radio_write_bytearray_to_file(data_bytearray)
            radio.radio.radio_append_bytearray_to_file(data_bytearray)

            # FRAMES
            print("Frames")
            hdlc_frames = hdlc.hdlc.hdlc_decode_bytes(data_bytearray)

            for i, frame in enumerate(hdlc_frames):
                print(f"Frame (bytearra) {i + 1}: {frame}")
                print(f"Frame (hex) {i + 1}: {frame.hex()}")

            # DECODE

            # fime: mulitple frames same time
            date_now = datetime.now()
            time_received_unix = datetime.timestamp(date_now)
            time_measurement_s = time_received_unix
            print("Decode")
            for i, frame in enumerate(hdlc_frames):
                frame_address = radio.radio.frame_get_hdlc_address(frame)
                print(f"Frame address: {frame_address}")
                frame_control = radio.radio.frame_get_hdlc_control(frame)
                print(f"Frame control: {frame_control}")
                #
                payload_version = radio.radio.frame_get_info_version(frame)
                print(f"Payload version: {payload_version}")
                #
                payload_content = radio.radio.frame_get_info_content(frame)
                payload = radio.radio.frame_get_data(frame)
                print(f"Payload (hex): {payload.hex()}")
                print(f"Payload (int): {int.from_bytes(payload, byteorder='little', signed=False)}")
                #
                # todo : remove last two bytes ?
                match payload_content:
                    case 2:
                        # temperature 1
                        print("temperature 1")
                        temperatures = radio.radio.get_temperature_values_degree(payload)
                        time_node_unix = radio.radio.get_temperature_time_unix(payload)
                        print(f"Temperatures: {temperatures}")
                        print(f"Time node unix: {time_node_unix}")
                        print(datetime.fromtimestamp(time_node_unix).strftime('%Y-%m-%d %H:%M:%S'))
                        # 
                        print("Database")
                        dbfilepath = r"gateway_v2.db"
                        # todo : get from frame
                        node_id = 10
                        # todo : get from frame
                        sensortype = 1
                        # todo : time sync/diff with node

                        for i, temperature in enumerate(temperatures):
                            if temperature:
                                time_measurement_s -= 5
                                insert_temperatures_into_database(dbfilepath,
                                                      node_id,
                                                      #time_received_unix_s,
                                                      time_measurement_s,
                                                      sensortype,
                                                      temperature)
                    case 3:
                        # temperature 2
                        print("temperature 2")
                    case _:
                        print("Invalid frame content")

        except Exception as e:
            print(f"An error occurred: {e}")

        # PLOT
        print("Plot")
        visualize.plot_database.plot_measurements()
        time.sleep(1)
        

    print("EXIT pc mode")
    #deinit_serial(self.serial_rc)
    #self.timer_repeated.stop()
    
    #radio_read(self.serial_rc)
    return


# todo : for v2
def insert_temperatures_into_database(dbfilepath, node_id, time_unix, sensortype, temperature):
    measurements = (
        node_id,
        time_unix,
        sensortype,
        temperature)
    with database.sqlite.DbConnection(dbfilepath) as db_connection:
        database.db_operation.insert_temperature_into_measurements(connection = db_connection, measurements = measurements)
    return None

def insert_temperatures_testdata_into_database(dbfilepath):
    with database.sqlite.DbConnection(dbfilepath) as db_connection:
        database.db_operation.insert_temperature_into_measurements(connection = db_connection, measurements = (10, 1234567890, 1, 25.0))
        database.db_operation.insert_temperature_into_measurements(connection = db_connection, measurements = (10, 1234567895, 1, 24.5))
        database.db_operation.insert_temperature_into_measurements(connection = db_connection, measurements = (10, 1234567900, 1, 24.0))
        database.db_operation.insert_temperature_into_measurements(connection = db_connection, measurements = (10, 1234567905, 1, 24.5))
    return None
