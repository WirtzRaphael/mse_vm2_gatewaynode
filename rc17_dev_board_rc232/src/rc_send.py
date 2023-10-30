import difflib
import pickle
import serial
import time
import rc232
import rc_serial
import rc_measurements

def rc_send():
    #serial_port = 'COM3'
    baud_rate = 19200 

    class SerialRcDevBoard:
        def __init__(self, port, baud_rate):
            self.port = port
            self.baud_rate = baud_rate

    dev_board_serial_10 = SerialRcDevBoard('/dev/ttyUSB1', baud_rate)
    dev_board_config_10 = rc232.RC232Configuration(channel=1, destination_id=20, power=0, rssi_mode=1, unique_id=10)

    serial_10 = rc_serial.serial_init(dev_board_serial_10.port, dev_board_serial_10.baud_rate)
    
    try:
        serial_10.open()

    except serial.SerialException as e:
        print(f"Serial communication error: {e}")

    
    send_packages = rc_measurements.get_test_data_set_send()
    rc_measurements.write_to_file(send_packages, "log/test_data_send.txt")
    
    file_ser = open("log/test_data_serialized.txt", "w")
    
    counter = 0
    for send_package in send_packages: 
        ##### SEND
        print("-- SERIALIZE")
        send_package_serialized = rc232.serialization(dev_board_config_10, send_package)
        file_ser.write(send_package_serialized + "\n")

        print("-- SEND")
        try:
            time.sleep(5)
            serial_10.write(send_package_serialized.encode()) # encode string to bytes
        except serial.SerialException as e:
            print(f"Serial communication error: {e}")
        counter = counter + 1
        print("counter: ", counter)
    
    file_ser.close()

    try:
        serial_10.close()
    except serial.SerialException as e:
        print(f"Serial communication error: {e}")
