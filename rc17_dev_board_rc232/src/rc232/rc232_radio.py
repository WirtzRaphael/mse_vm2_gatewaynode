import serial

def radio_receive(serial_object: serial.Serial):
    try:
        # fix : package size, no magik number
        received_package_bin = serial_object.read(37)
        received_package = received_package_bin.decode()
        #file_rec.write(received_package)
        print(f"Received data raw: {received_package}")
        return received_package
    except serial.SerialException as e:
        #print(f"Serial communication error: {e}")
        raise
