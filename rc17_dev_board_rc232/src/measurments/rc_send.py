import difflib
import pickle
import serial
import time
import rc232
import rc_serial
import rc_measurements

def rc_send(serial_object, rc232_config):
    #serial_port = 'COM3'
    
    send_packages = rc_measurements.get_test_data_set_send()
    rc_measurements.write_to_file(send_packages, "log/test_data_send.txt")
    
    file_ser = open("log/test_data_serialized.txt", "w")
    
    counter = 0
    for send_package in send_packages: 
        ##### SEND
        print("-- SERIALIZE")
        send_package_serialized = rc232.serialization(rc232_config, send_package)
        file_ser.write(send_package_serialized + "\n")

        print("-- SEND")
        try:
            time.sleep(5)
            serial_object.write(send_package_serialized.encode()) # encode string to bytes
        except serial.SerialException as e:
            print(f"Serial communication error: {e}")
        counter = counter + 1
        print("counter: ", counter)
    
    file_ser.close()

    try:
        serial_object.close()
    except serial.SerialException as e:
        print(f"Serial communication error: {e}")
