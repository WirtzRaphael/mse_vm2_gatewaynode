import serial
import time
import measurments.testdata
import rc232.rc232
import rc232.rc_serial

def rc_receive(serial_object, rc232_config):
    file_rec = open("log/test_data_received.txt", "w")
    counter = 1

    while(counter < 11):
        ##### RECEIVE
        print("-- RECEIVE")
        try:
            # fix : package size, no magik number
            received_package_bin = serial_object.read(37)
            received_package = received_package_bin.decode()
            file_rec.write(received_package)
            print(f"Received data: {received_package}")
        except serial.SerialException as e:
            print(f"Serial communication error: {e}")
        #time.sleep(0.1)
        print("counter", counter)
        counter = counter + 1

    file_rec.close()

    return

