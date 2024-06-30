import database.sqlite
import database.db_operation
import serial
import time
import os

temperature_min_degree = 1
DB_FILEPATH = r"gateway_v2.db"

# todo : in progress
# todo : buffer size
# todo : TEST
#todo: refactor bytearray one var
def radio_read(serial_object: serial.Serial):
    """ Read received serial data
    """
    try:
        #data = []
        data_byte = bytearray()

        with serial_object as ser:
            duration = 6  # Duration to read data in seconds
            start_time = time.time()
            while (time.time() - start_time) < duration:
                if ser.in_waiting > 0:
                    data_read = ser.read(ser.in_waiting)
                    #data.append(data_read)
                    data_byte.extend(data_read)
                    print(f"Received data: {data_read}")
                time.sleep(0.1)  # Small delay to avoid busy-waiting
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if ser.is_open:
            ser.close()


    print(f"Received data (byte): {data_byte}")
    #print(f"Received data (hex): {data[0].hex()}")

    return data_byte

    #received_byte_stream = serial_object.read(256)
    # if empty
    #if received_byte_stream == b'':
    #    print("Byte string is empty.")
    #    # todo : dont stop program
    #    return
    # RSSI - signal strength


def radio_write_bytearray_to_file(bytearray_data):
    try:
        output_file = 'serial_data.bin'
        with open(output_file, 'wb') as f:
            f.write(bytearray_data)
            print(f"Data written to file: {output_file}")
    except Exception as e:
        print(f"An error occurred: {e}")

    return

def radio_append_bytearray_to_file(bytearray_data):
    try:
        output_file = 'serial_data.bin'
        with open(output_file, 'ab') as f:
            f.write(bytearray_data)
            print(f"Data appended to file: {output_file}")
    except Exception as e:
        print(f"An error occurred: {e}")

    return

"""" Receive data and write to file
"""
def radio_receive_write_to_file(serial_object: serial.Serial):
    try:
        with serial_object as ser:
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

"""" Read received data from file
"""            
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


"""" Read binary file
"""
def read_binary_file(file_path):
    try:
        with open(file_path, 'rb') as f:
            return f.read()
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        return None
    
def frame_get_payload(frame:bytearray):
    # todo : check length try catch
    hdlc_address = frame[0]
    hdlc_control = frame[1] 

    # 1 byte : data info field
    data_info = frame[2]
    # 3 bit : version
    data_info_version = data_info >> 5
    # 5 bit : content
    data_info_content = data_info & 0b00011111

    # 1 byte : node address
    address_node = frame[3]

    # n byte : data
    payload = frame[4:-1]
    
    print(f"HDLC address: {hdlc_address}")
    print(f"HDLC control: {hdlc_control}")
    #
    print(f"Data info: {data_info}")
    print(f"Data info version: {data_info_version}")
    print(f"Data info content: {data_info_content}")
    print(f"Node address: {address_node}")
    print(f"Payload: {payload}")

    return payload

def get_temperature_values_degree(payload):
    # todo : time
    temperature_values_degree = []

    for i in range(0, len(payload), 2):
        # pass two bytes
        temperature_dec = temperature_convert_byte_to_dec(payload[i:i+2])
        temperature_degree = temperature_convert_dec_to_degree(temperature_dec)
        temperature_values_degree.append(temperature_degree)

    return temperature_values_degree


def temperature_convert_byte_to_dec(temperature:bytearray):
    if len(temperature) != 2:
        print("Invalid byte array length.")
        return
    
    return (temperature[0]) | temperature[1] << 8

def temperature_convert_dec_to_degree(temperature:int):
    # avoid type conflict
    if not isinstance(temperature, int):
        return None
    if (temperature >= temperature_min_degree * 100):
        return temperature / 100