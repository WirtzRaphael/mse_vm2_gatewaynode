import database.sqlite
import database.db_operation
import radio.packages
import rc232.testing
import rc232.config
import rc232.serial
import rc232.radio
import schedule 
from schedule import every, repeat
import serial
import timeutil.timer
import time

DB_FILEPATH = r"gateway_v2.db"


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
    
    # scheduling
    #self.timer_repeated = timeutil.timer.RepeatedTimer(1,radio_read, serial_rc) # auto-starts
    #schedule.every(1).seconds.do(radio_read, serial_rc) # sometimes conflict with serial port
    #schedule.every().day.at("00:00").do(time_sync)
    
    while(operation_mode == 'gateway_pc'):
        time.sleep(1)
        radio_read(serial_rc)
        #schedule.run_pending()
        

    print("EXIT pc mode")
    deinit_serial(self.serial_rc)
    #self.timer_repeated.stop()
    
    #radio_read(self.serial_rc)
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

# todo : use scheduler
def radio_read(serial_object: serial.Serial):
    try:
        received_stream = rc232.radio.radio_receive(serial_object)
        received_packages = radio.packages.split_into_packages(received_stream)
        if received_packages == None:
            return None
        pass
    except serial.SerialException as e:
        print(f"Serial communication error: {e}")
        
    received_payloads = list()
    for package in received_packages: 
        payload = radio.packages.payload_readout(package)
        received_payloads.append(payload)
    
    signal_strength_int = 0
    # RSSI - signal strength
    # fix : use received stream, package split could remove rssi value (;)
    # bug (?) : value maybe lesser than in RcTools (compare to explicit function with cmd 'S')
    for package in received_packages[-1:]:
        # last element
        if len(package) > 3:
            continue
        char = package
        if 'LF' in char:
            char = char.replace('LF', '')
        try:
            # last character (rssi) to int
            # todo : don't write converted value to database
            signal_strength_int = ord(char[-1])
        except:
            signal_strength_int = None

    with database.sqlite.DbConnection(DB_FILEPATH) as db_connection:
        for received_payload in received_payloads:
            if received_payload == None:
                continue     
            match received_payload:
                case radio.packages.ProtocolPayloadTemperature():
                    print("payload temperature")
                    insert_temperatures_into_database(db_connection, received_payload, signal_strength_int)
                case radio.packages.ProtocolPayloadStatus():
                    print("payloadsignal_strengthstatus")
                case _:
                    print("payload unknown")
                    continue
    return None

def insert_temperatures_into_database(db_connection:database.sqlite.DbConnection, payload:radio.packages.ProtocolPayloadTemperature, signal_strength:int):
    # todo : fix sql injection
    print("db  operation")
    #if payload.sensor_nr != None:
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