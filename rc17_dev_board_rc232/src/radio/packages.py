 
class PacketSendSensor:
    def __init__(self,id, content, timestamp):
        self.id = id
        self.timestamp = timestamp
        self.content = content
        self.separator = ';'
    def __repr__(self):
        return "{0},{1},{2}".format(self.id, self.timestamp, self.content)


class PacketReceiveSensor:
    def __init__(self,id, content, timestamp, rssi):
        self.id = id
        self.timestamp = timestamp
        self.content = content
        self.rssi = rssi

class PacketReceiveConfiguration:
    separator = '-J'
    packet_end_char = 'LF'

def serializationSensor(instance, data):
    # todo : packet size
    #string = str(data.id) + str(data.timestamp) + str(data.content) + str(data.separator)
    string = ""
    return string 

# todo : refactore more generalized
def deserializationSensor(data):
    packetConfig = PacketReceiveConfiguration()
    packet_list = data.split(packetConfig.separator)
    print(packet_list)

    for packet in packet_list:
        print("packet: ", packet)
    
    if data != "":
        packetReceived = PacketReceiveSensor() 
        packetReceived.id = data[:3]
        packetReceived.timestamp = data[3:20]
        packetReceived.content = data[21:-1]
        packetReceived.rssi = data[-1:]
        return packetReceived
    return

def print_packet_received(package):
    print("id: ", package.id)
    print("timestamp: ", package.timestamp)
    print("content: ", package.content)
    print("rssi: ", package.rssi)
