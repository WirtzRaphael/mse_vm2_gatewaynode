import database.sqlite
import database.db_operation
import serial
import time
import os


DB_FILEPATH = r"gateway_v2.db"

# todo : in progress
# todo : buffer size
# todo : TEST
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
        # receive stream
        # frames
        # packages
        pass
    except serial.SerialException as e:
        print(f"Serial communication error: {e}")
        
    # payload data
    
    # RSSI - signal strength
    return received_byte_stream


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
    
def frame_get_payload(frame):
    # todo : check length try catch

    # 1 byte : data info field
    data_info = frame[0]
    # 3 bit : version
    data_info_version = data_info >> 5
    # 5 bit : content
    data_info_content = data_info & 0b00011111

    # 1 byte : node address
    address_node = frame[1]

    # n byte : data
    data = frame[2:-1]
    print(f"Data info: {data_info}")
    print(f"Data info version: {data_info_version}")
    print(f"Data info content: {data_info_content}")
    print(f"Node address: {address_node}")
    print(f"Data: {data}")

    pass

