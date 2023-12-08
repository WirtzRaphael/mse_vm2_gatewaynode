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

class PacketReceiveSensorNew:
    def __init__(self):
        self.temperature1 = 0
        self.temperatureId1 = 0
        self.temperature2 = 0
        self.temperatureId2 = 0



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

    if data != "" and len(packet_list) >= 4:
        packetReceived = PacketReceiveSensorNew()
        packetReceived.temperature1 = packet_list[0]
        packetReceived.temperatureId1 = packet_list[1]
        packetReceived.temperature2 = packet_list[2]
        packetReceived.temperatureId2 = packet_list[3]
        return packetReceived
    return
    

def print_packet_received(package):
    print("id: ", package.id)
    print("timestamp: ", package.timestamp)
    print("content: ", package.content)
    print("rssi: ", package.rssi)
