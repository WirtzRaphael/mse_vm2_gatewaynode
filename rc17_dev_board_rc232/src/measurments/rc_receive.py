import serial
import time
import measurments.testdata
import rc232.config
import rc232.serial



def rc_receive(serial_object: serial.Serial, rc232_config):
    file_rec = open("log/test_data_received.txt", "w")
    counter = 1

    print("-- RECEIVE")
    while(counter < 20):
        ##### RECEIVE
        try:
            # fix : package size, no magik number
            received_package_bin = serial_object.read(38)
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

