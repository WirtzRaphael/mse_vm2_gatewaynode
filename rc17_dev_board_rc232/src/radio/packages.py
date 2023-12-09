# todo : obsolet
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
    payload_separator = '-'
    package_end_char = ';'
    rc_232_packet_end_char = 'LF'


# todo : refactore more generalized
def deserialization_sensor(data):
    packetConfig = PacketReceiveConfiguration()
    packet_list = data.split(packetConfig.package_end_char)
    print(packet_list)

    for packet in packet_list:
        print("packet: ", packet)
        payload_list = packet.split(packetConfig.payload_separator)
        print("payload_list: ", payload_list)
        # hint : payload list sometimes with more characters
        if data != "" and len(payload_list) >= 4:
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
