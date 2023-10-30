import serial
import time
import rc232
import rc_serial
import rc_measurements

def rc_receive():
    #serial_port = 'COM3'
    baud_rate = 19200 

    class SerialRcDevBoard:
        def __init__(self, port, baud_rate):
            self.port = port
            self.baud_rate = baud_rate

    dev_board_serial_20 = SerialRcDevBoard('/dev/ttyUSB0', baud_rate)
    dev_board_config_20 = rc232.RC232Configuration(channel=1, destination_id=10, power=0, rssi_mode=1, unique_id=20)

    serial_20 = rc_serial.serial_init(dev_board_serial_20.port, dev_board_serial_20.baud_rate)

    try:
        serial_20.open()

    except serial.SerialException as e:
        print(f"Serial communication error: {e}")

    
    file_rec = open("log/test_data_received.txt", "w")
    counter = 0

    while(counter < 11):
        ##### RECEIVE
        print("-- RECEIVE")
        try:
            # fix : package size, no magik number
            received_package_bin = serial_20.read(37)
            received_package = received_package_bin.decode()
            file_rec.write(received_package)
            print(f"Received data: {received_package}")
        except serial.SerialException as e:
            print(f"Serial communication error: {e}")
        #time.sleep(0.1)
        counter = counter + 1
        print("counter", counter)

    file_rec.close()

    try:
        serial_20.close()
    except serial.SerialException as e:
        print(f"Serial communication error: {e}")

    return

