import serial
# serial port
# eg linux '/dev/ttyUSB0'
# eg windows 'COM3'

class SerialRcDevBoard:
    def __init__(self, port, baud_rate, timeout):
        self.port = port
        self.baud_rate = baud_rate
        self.timeout = timeout


def serial_init(serial_port, baud_rate, timeout_s = 1):
    serial_object = serial.Serial(
        port=serial_port,
        baudrate=baud_rate,
        #startbits=serial.STARTBITS_ONE,
        stopbits=serial.STOPBITS_ONE,
        parity=serial.PARITY_NONE,
        xonxoff=0,      # flow control
        rtscts=1,       # rts/cts flow control
        dsrdtr=0,        # dsr/dtr flow control
        timeout=timeout_s
    )
    return serial_object
