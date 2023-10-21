import difflib
import serial
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
    sent_data = rc_measurements.get_test_string()
    sent_serialized = rc232.serialization(dev_board_config_10, sent_data)
    
    print("-- SEND")
    serial_10.write(sent_serialized.encode())

except serial.SerialException as e:
    print(f"Serial communication error: {e}")

finally:
    # Close the serial port when done
    serial_10.close()
    
##### RECEIVE
try:
    print("-- READ")
    # Read data from the device
    # todo : package size
    received_data = serial_20.read(15)
    received_data = received_data.decode()
    print(f"Received data: {received_data}")
    print("-- DESERIALIZE")
    received_deserialized = rc232.deserialization(dev_board_config_20, received_data)
    print("content: ", received_deserialized.content)
    print("rssi: ", received_deserialized.rssi)
    # Read data from the device

except serial.SerialException as e:
    print(f"Serial communication error: {e}")

finally:
    # Close the serial port when done
    serial_20.close()

##### COMPARE
print("-- COMPARE")
for received_string in received_data:
    output_list = [li for li in difflib.ndiff(sent_data, received_data) if li[0] != ' ']
    print(output_list)


print("End of program.")
