
# independent settins
baud_rate = 5
data_rate = 4 
sleep_mode = 0
high_power_temp_compensation = 0

class RC232Configuration:
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
        self.packet_end_character = 0
        self.address_mode = 2
        self.crc_mode = 2
        self.unique_id = unique_id
        self.system_id = 1
        self.destination_id = destination_id
        self.broadcast_address = 255
        self.high_power_temp_compensation = high_power_temp_compensation
        self.uart_baud_rate = baud_rate
        self.uart_flow_ctrl = 0
        self.data_interface = 0
        self.encryption_flag = 0
        self.decryption_flag = 0
 
 
class RC232PacketSend:
    def __init__(self,id, content, timestamp):
        self.id = id
        self.timestamp = timestamp
        self.content = content
    def __repr__(self):
        return "{0},{1},{2}".format(self.id, self.timestamp, self.content)


class RC232PacketReceive:
    def __init__(self,id, content, timestamp, rssi):
        self.id = id
        self.timestamp = timestamp
        self.content = content
        #self:crc
        self.rssi = rssi
        
# todo : rename class 
def serialization(instance, data):
    # todo : packet size
    string = str(data.id) + str(data.timestamp) + str(data.content)
    return string 

def deserialization(instance, data):
    if (instance.rssi_mode == 1):
        # todo : id (test)
        # todo : time
        RC232PacketReceive.id = data[:3]
        RC232PacketReceive.timestamp = data[3:20]
        RC232PacketReceive.content = data[-17:-1]
        RC232PacketReceive.rssi = data[-1:]
    else:

        RC232PacketReceive.content = data

    return RC232PacketReceive

