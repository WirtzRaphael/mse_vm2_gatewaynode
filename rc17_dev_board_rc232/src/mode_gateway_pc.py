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

SERIAL_PORT_RC_DEVBOAD = '/dev/ttyUSB2'
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
    with database.sqlite.DbConnection(db_file) as db_connection:
        if db_connection is not None:
            database.sqlite.create_table(connection = db_connection,
                                create_table_sql = database.db_operation.SQL_CREATE_GATEWAYNODE_TABLE)
            database.sqlite.create_table(connection = db_connection,
                                create_table_sql = database.db_operation.SQL_CREATE_SENSORNODES_TABLE)
            database.sqlite.create_table(connection = db_connection,
                                create_table_sql = database.db_operation.SQL_CREATE_TEMPERATURE_1_TABLE)
            database.sqlite.create_table(connection = db_connection,
                                create_table_sql = database.db_operation.SQL_CREATE_TEMPERATURE_2_TABLE)
    return None

""" Functions
"""
def run_mode_gateway_pc(operation_mode):
    print("RUN pc mode \n")
    #self.timer_repeated = None
    #self.serial_rc = None
    # initalization
    serial_rc = init_serial(serial_port= SERIAL_PORT_RC_DEVBOAD)
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

    with database.sqlite.DbConnection(DB_FILEPATH) as db_connection:
        for received_payload in received_payloads:
            if received_payload == None:
                continue     
            match received_payload:
                case radio.packages.ProtocolPayloadTemperature():
                    print("payload temperature")
                    insert_temperatures_into_database(db_connection, received_payload)
                case radio.packages.ProtocolPayloadStatus():
                    print("payload status")
                case _:
                    print("payload unknown")
                    continue
    return None

def insert_temperatures_into_database(db_connection:database.sqlite.DbConnection, payload):
    # todo : fix sql injection
    print("db  operation") 
    if payload.sensor_nr == '1':
        for sensorTemperature in payload.sensorTemperatureValues:
            database.db_operation.insert_temperature_into_temperature1(connection = db_connection,
                                                        measurement_temperature = (
                                                            payload.timestampRtc,
                                                            sensorTemperature.time_relative_to_reference,
                                                            sensorTemperature.temperatureId,
                                                            sensorTemperature.temperature))
    if payload.sensor_nr == '2':
        for sensorTemperature in payload.sensorTemperatureValues:
            database.db_operation.insert_temperature_into_temperature2(connection = db_connection,
                                                        measurement_temperature = (
                                                            payload.timestampRtc,
                                                            sensorTemperature.time_relative_to_reference,
                                                            sensorTemperature.temperatureId,
                                                            sensorTemperature.temperature))
    return