import difflib
import pickle
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

    while(1):
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
        time.sleep(0.1)

    file_rec.close()

    print("---- DESERIALIZE")
    file_rec = open("log/test_data_received.txt", "r")
    data_rec = file_rec.read()
    packages_rec = data_rec.split(";@")
    #packages_rec = data_rec.split(";<") # modules modifies special char 

    file_deser = open("log/test_data_deserialized.txt", "w")
    for package in packages_rec:
        received_package_deserialized = rc232.deserialization(dev_board_config_10, package)
        rc_measurements.append_to_file(received_package_deserialized, "log/test_data_deserialized.txt")
        rc232.print_packet_received(received_package_deserialized)
    file_deser.close()

    print("---- PROCESS")
    for package in list_packages_deser:
        separator = ';'
        with open("log/test_data_processed.txt", "w") as file_proc:
            timestamp_iso = rc_measurements.convert_time_utc_to_iso(float(package.timestamp))
            value = int(package.content, 2) # convert binary to int
            packet_str = f'''{package.id},
                {package.timestamp_iso},
                {package.value},
                {package.rssi}{separator}\n"
                '''

    try:
        serial_20.close()
    except serial.SerialException as e:
        print(f"Serial communication error: {e}")

    return

