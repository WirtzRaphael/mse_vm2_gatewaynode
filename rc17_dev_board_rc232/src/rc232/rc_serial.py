import serial
# serial port
# eg linux '/dev/ttyUSB0'
# eg windows 'COM3'

def serial_init(serial_port, baud_rate):
    serial_object = serial.Serial(
        port=serial_port,
        baudrate=baud_rate,
        stopbits=serial.STOPBITS_ONE,
        parity=serial.PARITY_NONE,
        xonxoff=0,      # flow control
        rtscts=0,       # rts/cts flow control
        dsrdtr=0        # dsr/dtr flow control
    )
    return serial_object
