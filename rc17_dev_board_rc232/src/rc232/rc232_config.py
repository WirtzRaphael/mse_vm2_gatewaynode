import rc232.rc232
import serial

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



