import difflib
import pickle
import serial
import time
import rc232
import rc_serial
import rc_measurements

#serial_port = 'COM3'
baud_rate = 19200 

class SerialRcDevBoard:
    def __init__(self, port, baud_rate):
        self.port = port
        self.baud_rate = baud_rate

dev_board_serial_10 = SerialRcDevBoard('/dev/ttyUSB0', baud_rate)
dev_board_config_10 = rc232.RC232Configuration(channel=1, destination_id=20, power=0, rssi_mode=1, unique_id=10)
dev_board_serial_20 = SerialRcDevBoard('/dev/ttyUSB1', baud_rate)
dev_board_config_20 = rc232.RC232Configuration(channel=1, destination_id=10, power=0, rssi_mode=1, unique_id=20)

serial_10 = rc_serial.serial_init(dev_board_serial_10.port, dev_board_serial_10.baud_rate)
serial_20 = rc_serial.serial_init(dev_board_serial_20.port, dev_board_serial_20.baud_rate)

try:
    serial_10.open()

except serial.SerialException as e:
    print(f"Serial communication error: {e}")

try:
    serial_20.open()

except serial.SerialException as e:
    print(f"Serial communication error: {e}")
  
  
send_packages = rc_measurements.get_test_data_set_send()
rc_measurements.write_to_file(send_packages, "log/test_data_send.txt")
 
file1 = open("log/test_data_serialized.txt", "a")
file2 = open("log/test_data_received.txt", "a")
 
for send_package in send_packages: 
    ##### SEND
    print("-- SERIALIZE")
    send_package_serialized = rc232.serialization(dev_board_config_10, send_package)
    file1.write(send_package_serialized + "\n")

    print("-- SEND")
    try:
        serial_10.write(send_package_serialized.encode()) # encode string to bytes
    except serial.SerialException as e:
        print(f"Serial communication error: {e}")
  
    ##### RECEIVE
    print("-- RECEIVE")
    try:
        # fix : package size, no magik number
        received_package_bin = serial_20.read(32)
        received_package = received_package_bin.decode()
        file2.write(received_package + "\n")
        print(f"Received data: {received_package}")
    except serial.SerialException as e:
        print(f"Serial communication error: {e}")

    print("---- DESERIALIZE")
    received_package_deserialized = rc232.deserialization(dev_board_config_10, received_package)
    print("id: ", received_package_deserialized.id)
    print("timestamp: ", received_package_deserialized.timestamp)
    print("content: ", received_package_deserialized.content)
    print("rssi: ", received_package_deserialized.rssi)
    
    rc_measurements.append_to_file(received_package_deserialized, "log/test_data_deserialized.txt")
    

file1.close()
file2.close()

try:
    serial_10.close()
except serial.SerialException as e:
    print(f"Serial communication error: {e}")

try:
    serial_20.close()
except serial.SerialException as e:
    print(f"Serial communication error: {e}")


##### COMPARE
#print("-- COMPARE")
#for received_string in received_data:
#    output_list = [li for li in difflib.ndiff(sent_data, received_data) if li[0] != ' ']
#    print(output_list)
#

print("End of program.")
