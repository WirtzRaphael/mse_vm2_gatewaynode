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
  

##### SEND
try:
    print("-- SERIALIZE")
    #sent_data = rc_measurements.get_test_string()
    send_data_set = rc_measurements.get_test_data_set_send()
    rc_measurements.write_to_file(send_data_set)
    
    print("-- SEND")
    # todo : rename to packet
    with open("test_data_serialized.txt", "w") as file:
        for send_data in send_data_set:
            send_serialized = rc232.serialization(dev_board_config_10, send_data)
            #send_serialized = pickle.dumps(send_data)
            serial_10.write(send_serialized.encode()) # encode string to bytes
            file.write(send_serialized + "\n")
            time.sleep(0.01)

except serial.SerialException as e:
    print(f"Serial communication error: {e}")

##### RECEIVE
try:
    print("-- READ")
    # Read data from the device
    # fix : package size, no magik number
    # fix : timeout, buffer size limit (fifo)
    for i in range(0, 99):
        received_data = serial_20.read(32)
        received_data = received_data.decode()
        print(f"Received data: {received_data}")
        print("---- DESERIALIZE")
        received_deserialized = rc232.deserialization(dev_board_config_10, received_data)
        print("id: ", received_deserialized.id)
        print("timestamp: ", received_deserialized.timestamp)
        print("content: ", received_deserialized.content)
        print("rssi: ", received_deserialized.rssi)

except serial.SerialException as e:
    print(f"Serial communication error: {e}")


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
