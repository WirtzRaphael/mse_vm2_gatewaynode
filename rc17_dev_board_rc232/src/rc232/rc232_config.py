import rc232.rc232
import serial
import time

# independent settins
baud_rate = 5
data_rate = 4 
sleep_mode = 0
high_power_temp_compensation = 0

class RC232Configuration:
    rf_channel = {
        1: 169.406250,
        2: 169.418750,
        3: 169.431250,
        4: 169.443750,
        5: 169.456250,
        6: 169.468750,
        7: 169.412500,
        8: 169.437500,
        9: 169.462500
    }
    rf_data_rate = {
        1: "TBD",
        2: "0.3kbit/s",
        3: "0.6kbit/s",
        4: "1.2kbit/s",
        5: "2.4kbit/s",
        6: "TBD",
        7: "4.8kbit/s",
        8: "9.6kbit/s",
        9: "TBD",
        10:"19.2kbit/s",
        11:" TBD",
        12:"38.4kbit/s",
        13:"50kbit/s",
        14:"76.8kbit/s",
        15:"100kbit/s"
    }
    rf_power = {
        1: "14dbm",
        2: "17dbm",
        3: "20dbm",
        4: "24dbm",
        5: "27dbm"
    }
    sleep_mode = {
        0: "Disabled",
        1: "Not in use",
        2: "Enable SLEEP pin"
    }
    rssi_mode = {
        0: "Disabled",
        1: "Enabled"
    }
    # Time before modem timeout and transmit buffered data.
    # 0-254
    # None means packet timeout is disabled. Use packet length or end character instead.
    packet_timeout = {
        0: 0,
        1: 32,
        2: 48,
        3: 64,
        #...
        124: 2000, 
        #...
        249: 4000,
        254: 4080
    }
    packet_end_character = {
        # ASCII character.
        0: "None",
        10: "LF",
        13: "CR",
        90: "Z"
    }
    # using addressing adds SYSTEM ID and DESTINATION ID to the packet. 
    address_mode = {
        0: "No addressing (default)",
        2: "Use addressing"
    }
    crc_mode = {
        0: "No CRC", # in transparent mode
        2: "CRC-16"  # default
    }
    # HP_TEMPCOMP
    high_power_temp_compensation = {
        0: "Disabled", # default
        1: "Enabled" 
    }

    # attention : if changing host may loose contact with module.
    # does not take effect until module is re-booted / reset.
    # not listed baudrate can be typed in manually.
    uart_baud_rate = {
        0: "Not used",
        1: "2400",
        2: "4800",
        3: "9600",
        4: "14400",
        5: "19200", # default
        6: "28800",
        7: "38400",
        8: "56700",
        9: "76800",
        10: "115200",
        11: "230400"
    }

    uart_flow_ctrl = { 
        0: "None (default)",
        1: "CTS only",
        2: "RTS only",
        3: "CTS / RTS",
        4: "RXTX (RS485)"
    }
    
    data_interface = {
        32: "UART header type length+power+channel in Tx"
    }


# todo : move
# When enabled the module will enter sleep on SLEEP pin low.
# Do not use in combination with UART handshake.
    def __init__(
        self,
        channel,
        destination_id,
        power,
        rssi_mode,
        unique_id):
        self.channel = channel
        self.power = power
        self.data_rate = data_rate
        self.sleep_mode = sleep_mode
        self.rssi_mode = rssi_mode
        self.packet_length = 128
        self.packet_timeout = 124
        self.packet_end_character = 10 # 0: none, 10: LF (\n), 13: CR (\r), 90: Z
        self.address_mode = 2
        self.crc_mode = 2
        self.unique_id = unique_id
        self.system_id = 1
        self.destination_id = destination_id
        self.broadcast_address = 255
        self.high_power_temp_compensation = high_power_temp_compensation
        self.uart_baud_rate = baud_rate
        self.uart_flow_ctrl = 3 # 0: none, 1: cts, 2: rts, 3: rtc/cts
        self.data_interface = 0
        self.encryption_flag = 0
        self.decryption_flag = 0
        
        
def rc232_config_init(serial_object: serial.Serial, rc232_config):
    return

# ==== FLOW DIAGRAM ====
#
#             | Idle | <-------------------------------+
#                 |                                    |
#        | Pull CONFIG pin low |                       |
#                 |                                    |
#        | Wait for '>' on TXD |                       |
#                 |                                    |
#   +--> | Send command byte to RXD |                  |
#   |             |                                    |
#   |    | Wait for '>' on TXD |                       |
#   |             |                                    |
#   |    | Send command parameters to RXD |            |
#   |             |                                    |
#   |    | Wait for '>' on TXD |                       |
#   |             |                                    |
#   +--- Yes <- New command ? -> No -> Send X to RXD --+
#
# ===== MEMORY =====
# - volatile configuration memory (RAM)
# - non volatile configuration memory (Flash)

# todo : reduce arguments
def config_cmd(serial_object: serial.Serial, cmd, dryrun:bool, cmd_type="char", argument=None, arg_type="int", return_value=False):
    try:
        __exit_config_mode(serial_object)
        # wait : pull CONFIG pin low
        __wait_module_response_prompt_blocking(serial_object, dryrun)
        if cmd_type == "hex":
            __send_command_data_hex(serial_object, cmd, dryrun)
        else:
            __send_command_data_char(serial_object, cmd, dryrun)

        if argument is not None:
            __wait_module_response_prompt_blocking(serial_object, dryrun)
            if arg_type == "hex":
                __send_command_data_hex(serial_object, argument, dryrun)
            else:
                __send_command_data_int(serial_object, argument, dryrun)
            __wait_module_response_prompt_blocking(serial_object, dryrun)

        if return_value == True:
            module_response = __wait_module_response_value_blocking(serial_object, dryrun)
            return module_response

    except TimeoutError as err:
        return
    except serial.SerialException as e:
        return
    return

# fixme : not working
def config_non_volatile(serial_object: serial.Serial, dryrun:bool):
    config_cmd(serial_object, "M", argument=None, dryrun=dryrun)
    # adress
    # todo: replace example
    __send_command_data_hex(serial_object, 0x01, dryrun)
    __send_command_data_int(serial_object, 1, dryrun)
    # exit
    __send_command_data_hex(serial_object, 0xFF, dryrun)
    __wait_module_response_prompt_blocking(serial_object, dryrun)
    print("config set memory finished")
    return

def read_temperature(serial_object: serial.Serial, dryrun:bool):
    try:
        # todo replace with config cmd
        __exit_config_mode(serial_object)
        __wait_module_response_prompt_blocking(serial_object, dryrun)
        __send_command_data_char(serial_object, "U", dryrun)
        module_response = __wait_module_response_value_blocking(serial_object, dryrun)
    except TimeoutError as err:
        return
    if b'>' in module_response:
        #print("The character '>' is present in the binary data.")
        cleaned_response = module_response.replace(b'>', b'')
        #print(cleaned_response)
        cleaned_response_int = int.from_bytes(cleaned_response, byteorder='big')
        return (cleaned_response_int - 128)
    return

# todo: check if working
def set_rf_power(serial: serial.Serial, power:int):
    print("set rf power to: ", power)
    if (power < 1 or power > 5):
        print("error: power out of range")
        return
    config_cmd(serial, "P", argument=power, dryrun=False)
    return

# fixme: not example
def read_memory_one_byte(serial_object: serial.Serial, dryrun:bool):
    address = 0x01
    module_response = config_cmd(serial_object, "Y", argument=address, arg_type="hex", return_value=True, dryrun=dryrun)
    print("address", address, "; value: ", module_response)
    return 

def rc232_reset_module():
    # todo : implement
    return

def read_voltage(serial_object: serial.Serial, dryrun:bool=False):
    try:
        #module_response = config_cmd(serial_object, cmd_str="V", dryrun=dryrun, argument=None, return_value=True)
        module_response = config_cmd(serial_object, cmd=0x56, cmd_type="hex", dryrun=dryrun, argument=None, return_value=True)
        if module_response is not None and b'>' in module_response:
            #print("The character '>' is present in the binary data.")
            cleaned_response = module_response.replace(b'>', b'')
            #print(cleaned_response)
            cleaned_response_int = int.from_bytes(cleaned_response, byteorder='big')
            return (cleaned_response_int * 0.03)
    except TimeoutError as err:
        return
    return

def __wait_module_response_blocking(serial_object: serial.Serial, decode:bool):
    print("wait for module response")
    timeout = 10
    timeout_start = time.time()
    while time.time() < timeout_start + timeout:
        if (serial_object.in_waiting > 0):
            if(decode == True):
                serial_val = serial_object.read(serial_object.in_waiting).decode()
            else:
                serial_val = serial_object.read(serial_object.in_waiting)
            #print("READ: ", serial_val)
            return serial_val
    raise TimeoutError("module not responding")

def __wait_module_response_value_blocking(serial_object: serial.Serial, dryrun:bool):
    if(dryrun == True):
        print("dryrun: skip module response value")
        return
    try:
        module_response = __wait_module_response_blocking(serial_object, decode=False)
        return module_response
    except TimeoutError as err:
        print("TimeoutError: ", err)
        raise

# wait for '>' on TXD
def __wait_module_response_prompt_blocking(serial_object: serial.Serial, dryrun:bool):
    if(dryrun == True):
        print("dryrun: skip module response check")
        return
    try:
        module_response = __wait_module_response_blocking(serial_object, decode=True)
        if (module_response == '>'):
            print("module reponding")
    except TimeoutError as err:
        print("TimeoutError: ", err)
        raise

def __send_command_data_char(serial_object: serial.Serial, command, dryrun:bool):
    command_encode = command.encode()
    if(dryrun == True):
        print("dryrun: ", command_encode)
        return
    print("send data char: ", command_encode)
    serial_object.write(command_encode)
    return

def __send_command_data_int(serial_object: serial.Serial, data_int:int, dryrun:bool):
    if(dryrun == True):
        print("dryrun: ", data_int)
        return
    print("send data: ", data_int)
    serial_object.write(data_int) # no encoding for int
    return

def __send_command_data_hex(serial_object: serial.Serial, address_hex:hex, dryrun:bool):
    binary_data = address_hex.to_bytes(1, byteorder='big') # 1 byte
    if(dryrun == True):
        print("dryrun: ", binary_data)
        return
    print("send data binary string: ", binary_data)
    serial_object.write(binary_data)
    return

def __exit_config_mode(serial_object: serial.Serial):
    serial_object.write('X'.encode())
    return
