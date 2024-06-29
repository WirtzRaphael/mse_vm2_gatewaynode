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

# todo : in progress
@repeat(every(5).seconds)
def radio_read(serial_object: serial.Serial):
    """ Read received serial data
    """
    try:
        # receive stream
        # frames
        # packages
        pass
    except serial.SerialException as e:
        print(f"Serial communication error: {e}")
        
    # payload data
    
    # RSSI - signal strength
   
    with database.sqlite.DbConnection(DB_FILEPATH) as db_connection:
        # insert into database
        return None

# todo : in progress
def radio_read_file():
    """Read received serial data from file
    """
    try:
        # todo : remove
        current_path = os.getcwd()
        print("Current working directory:", current_path)
        #
        filepath = "rc17_dev_board_rc232/examples/serial_packages_one_package.txt"
        with open(filepath, "r") as file:
            received_data = file.read()
        
        # convert hex to binary
        received_stream = bytes.fromhex(received_data)
        if not isinstance (received_stream, bytes):
            raise TypeError("Received data is not bytes")

        # HDLC frame delimiter is typically 0x7E
        FRAME_DELIMITER = b'\x7e'
        # Split data into frames using the delimiter
        frames = re.findall(FRAME_DELIMITER, received_stream)
        # Remove empty frames
        frames = [frame for frame in frames if frame != '']           
        print(f"Frames : {frames}")

        for frame in frames:
            # parse with yahdlc
            data, ftype, seq_no = yahdlc.get_data(frame)
            print(f"Data : {data}, Frame type : {ftype}, Sequence number : {seq_no}")
        #data, ftype, seq_no = get_data(ser.read(ser.in_waiting))

        #received_stream = rc232.radio.radio_receive_file("rc17_dev_board_rc232/examples/received_serial_one_package_hex.txt")
        #received_packages = radio.packages.split_into_packages(received_stream)
        print("Radio read complete")

    except Exception as e:
        print(f"Radio read file error: {e}")

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