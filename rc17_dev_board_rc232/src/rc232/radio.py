import serial

def radio_receive(serial_object: serial.Serial):
    try:
        # fix : package size, no magik number
        received_stream_bin = serial_object.read(150)
        # fix : utf-8 conversion failure (0x08 etc.)
        received_stream = received_stream_bin.decode()
        #file_rec.write(received_package)
        print(f"Received data raw: {received_stream}")
        return received_stream
    except serial.SerialException as e:
        #print(f"Serial communication error: {e}")
        raise
