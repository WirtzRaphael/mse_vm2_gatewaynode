class PacketSendSensor:
    def __init__(self,id, content, timestamp):
        self.id = id
        self.timestamp = timestamp
        self.content = content
        self.separator = ';'
    def __repr__(self):
        return "{0},{1},{2}".format(self.id, self.timestamp, self.content)


class PacketReceiveSensor:
    def __init__(self, temperature1, temperatureId1, temperature2, temperatureId2):
        self.temperature1 = temperature1
        self.temperatureId1 = temperatureId1
        self.temperature2 = temperature2
        self.temperatureId2 = temperatureId2



class PacketReceiveConfiguration:
    separator = '-J'
    packet_end_char = 'LF'

def serialization_sensor(instance, data):
    # todo : packet size
    #string = str(data.id) + str(data.timestamp) + str(data.content) + str(data.separator)
    string = ""
    return string 


# todo : refactore more generalized
def deserialization_sensor(data):
    packetConfig = PacketReceiveConfiguration()
    packet_list = data.split(packetConfig.separator)
    print(packet_list)

    for packet in packet_list:
        print("packet: ", packet)

    # hint : packet list sometimes with more characters
    if data != "" and len(packet_list) >= 4:
        packetReceived = PacketReceiveSensor(
            temperature1 = packet_list[0],
            temperatureId1 = packet_list[1],
            temperature2 = packet_list[2],
            temperatureId2 = packet_list[3]
        )
        return packetReceived
    return
    

def print_packet_received_sensor(package):
    print("temperature1: ", package.temperature1)
    print("temperature1 Id: ", package.temperatureId1)
    print("temperature2: ", package.temperature2)
    print("temperature2 Id: ", package.temperatureId2)
