import database.sqlite
import database.db_operation
import radio.packages
import rc232.testing
import rc232.config
import rc232.serial
import rc232.radio
import schedule 
from schedule import every, repeat
import os
import re
import pandas as pd
from sqlalchemy import create_engine
import plotnine as p9
import serial
import timeutil.timer
import time
from sys import exit as sys_exit
from sys import stderr
from time import sleep
from yahdlc import (
    FRAME_ACK,
    FRAME_DATA,
    FRAME_NACK,
    FCSError,
    MessageError,
    frame_data,
    get_data,
)


# todo : duplication
SERIAL_PORT = '/dev/ttyUSB0'
SERIAL_BAUDRATE = 19200
SERIAL_TIMEOUT = 0

DB_FILEPATH = r"gateway_v2.db"
sqlengine = create_engine(f'sqlite:///{DB_FILEPATH}', echo=False)

""" Initialzation
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
        binary_data = read_received_data_from_file()
        hdlc_frames = hdlc_decode(binary_data)

        for i, frame in enumerate(hdlc_frames):
            print(f"Frame {i + 1}: {frame.hex()}")

        #radio_read_hdlc()
        #radio_read(serial_rc)

        #plot_measurements()
        time.sleep(1)
        

    print("EXIT pc mode")
    #deinit_serial(self.serial_rc)
    #self.timer_repeated.stop()
    
    #radio_read(self.serial_rc)
    return

# todo : move file
def hdlc_decode(data):
    frames = []
    frame = []
    escape = False
    in_frame = False

    for byte in data:
        if byte == 0x7E:  # Flag sequence
            if in_frame and frame:
                frames.append(bytes(frame))
                frame = []
            in_frame = not in_frame
            continue

        if in_frame:
            if byte == 0x7D:  # Escape character
                escape = True
                continue
            if escape:
                byte ^= 0x20
                escape = False
            frame.append(byte)

    return frames

def radio_receive_write_to_file():
    try:
        with serial.Serial(SERIAL_PORT, SERIAL_BAUDRATE, timeout=SERIAL_TIMEOUT) as ser:
            output_file = 'serial_data.bin'
            duration = 60  # Duration to read data in seconds
            start_time = time.time()
            with open(output_file, 'wb') as f:
                print(f"Saving data to: {output_file}")
                while (time.time() - start_time) < duration:
                    if ser.in_waiting > 0:
                        data = ser.read(ser.in_waiting)
                        f.write(data)
                        print(f"Received data: {data}")
                    time.sleep(0.1)  # Small delay to avoid busy-waiting
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if ser.is_open:
            ser.close()

def read_binary_file(file_path):
    try:
        with open(file_path, 'rb') as f:
            return f.read()
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        return None

def read_received_data_from_file():
    # todo : move
    # Read the binary data

    current_path = os.getcwd()
    print("Current working directory:", current_path)

    #filepath = "rc17_dev_board_rc232/examples/serial_packages_one_package.txt"
    file_path = './rc17_dev_board_rc232/examples/serial_data.bin'
    binary_data = read_binary_file(file_path)
    #binary_data = read_binary_file(filepath)

    if binary_data:
        print("Binary data read successfully.")
        return binary_data
    else:
        print("Failed to read binary data.")
        raise Exception("Failed to read binary data.")

def radio_read_hdlc():
    try:
        with serial.Serial(SERIAL_PORT, SERIAL_BAUDRATE, timeout=SERIAL_TIMEOUT) as ser:
            # -------------------------------------------------- #
            # Wait for HDLC frame
            # -------------------------------------------------- #
            print("[*] Waiting for data...")

            while True:
                try:
                    # 200 µs
                    sleep(200 / 1000000.0)
                    received_data = ser.read(ser.in_waiting)
                    data, ftype, seq_no = get_data(received_data)
                    break
                except MessageError:
                    # No HDLC frame detected.
                    pass
                except FCSError:
                    stderr.write("[x] Bad FCS\n")

                    print("[*] Sending NACK...")
                    ser.write(frame_data("", FRAME_NACK, 0))
                    sys_exit(0)
                except KeyboardInterrupt:
                    print("[*] Bye!")
                    sys_exit(0)

            # -------------------------------------------------- #
            # Handle HDLC frame received
            # -------------------------------------------------- #
            FRAME_ERROR = False

            if ftype != FRAME_DATA:
                stderr.write(f"[x] Bad frame type: {ftype}\n")
                FRAME_ERROR = True
            else:
                print("[*] Data frame received")

            if seq_no != 0:
                stderr.write(f"[x] Bad sequence number: {seq_no}\n")
                FRAME_ERROR = True
            else:
                print("[*] Sequence number OK")

            if FRAME_ERROR is False:
                print("[*] Sending ACK ...")
                ser.write(frame_data("", FRAME_ACK, 1))
            else:
                print("[*] Sending NACK ...")
                ser.write(frame_data("", FRAME_NACK, 0))
    except serial.SerialException as err:
        sys_exit(f"[x] Serial connection problem: {err}")

# todo : in progress
# todo : buffer size
def radio_read(serial_object: serial.Serial):
    """ Read received serial data
    """
    try:
        #received_buffer = rc232.radio.radio_receive_binary(serial_object)
        received_byte_stream = serial_object.read(256)
        # if empty
        if received_byte_stream == b'':
            print("Byte string is empty.")
            # todo : dont stop program
            return
        data, ftype, seq_no = yahdlc.get_data(received_byte_stream)
        print(f"Data : {data}, Frame type : {ftype}, Sequence number : {seq_no}")
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


# todo : delete
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

#@repeat(every(5).seconds)
def plot_measurements():
    # test data
    #measurements_temperature = {
    #    'time_unix_s': [1609459200, 1609462800, 1609466400, 1609470000],
    #    'sensor_value': [23.5, 24.0, 22.8, 23.1],
    #    'node_id': [10, 10, 10, 10]
    #}
    #measurements_temperature_df = pd.DataFrame(measurements_temperature)

    # data from database
    measurements_temperature_df = database.db_operation.read_temperature_df_from_measurements(engine = sqlengine, node_id = 10, limit = 10)
    print(measurements_temperature_df.head())
    # convert unix time to datetime
    measurements_temperature_df['time'] = pd.to_datetime(measurements_temperature_df['time_unix_s'], unit='s')

    plot_temperature = (
    p9.ggplot(
        measurements_temperature_df,
        p9.aes(
            x="time",
            y="sensor_value",
            color="factor(node_id)"  # Optional: add color by node_id
        ),
    )
    + p9.geom_line(linetype="dashed")
    + p9.geom_point()
    + p9.labs(
        title="Temperature Measurements",
        x="Time",
        y="Temperature (°C)",
        color="Node ID"
    )
    + p9.theme_minimal()
)
    plot_temperature.show()
    
    return None