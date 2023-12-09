

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
    # todo : only use temperature and id pair
    def __init__(self, timertc, temperature1, temperatureId1, temperature2, temperatureId2, temperature3, temperatureId3):
        self_timerRtc = timertc
        self.temperature1 = temperature1
        self.temperatureId1 = temperatureId1
        self.temperature2 = temperature2
        self.temperatureId2 = temperatureId2
        self.temperature3 = temperature3
        self.temperatureId3 = temperatureId3


class PacketReceiveConfiguration:
    payload_separator = '-'
    package_end_char = ';'
    rc_232_packet_end_char = 'LF'


def split_into_packages(packages):
    # todo : implement (see split package below)
    pass

# todo : refactore more generalized
def deserialization_sensor(packages):
    if packages == "":
        return
    packetConfig = PacketReceiveConfiguration()
    packet_list = packages.split(packetConfig.package_end_char)

    for packet in packet_list:
        payload_list = packet.split(packetConfig.payload_separator)
        # hint : payload list sometimes with more characters
        if len(payload_list) >= 4:
            packetReceived = PacketReceiveSensor(
                timertc = payload_list[0],
                # todo : avoid hardcoding, dynamic payload size (out of range), try catch
                temperature1 = payload_list[1],
                temperatureId1 = payload_list[2],
                temperature2 = payload_list[3],
                temperatureId2 = payload_list[4],
                temperature3 = payload_list[5],
                temperatureId3 = payload_list[6],
            )
            return packetReceived
        return
    

def print_packet_received_sensor(package):
    print("temperature1: ", package.temperature1)
    print("temperature1 Id: ", package.temperatureId1)
    print("temperature2: ", package.temperature2)
    print("temperature2 Id: ", package.temperatureId2)
