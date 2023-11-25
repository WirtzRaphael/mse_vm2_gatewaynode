



 
 
class RC232PacketSendTesting:
    def __init__(self,id, content, timestamp):
        self.id = id
        self.timestamp = timestamp
        self.content = content
        self.separator = ';'
    def __repr__(self):
        return "{0},{1},{2}".format(self.id, self.timestamp, self.content)


class RC232PacketReceiveTesting:
    def __init__(self,id, content, timestamp, rssi):
        self.id = id
        self.timestamp = timestamp
        self.content = content
        self.rssi = rssi
        self.separator = ';'
        
# todo : rename class 
def serializationTesting(instance, data):
    # todo : packet size
    string = str(data.id) + str(data.timestamp) + str(data.content) + str(data.separator)
    return string 

def deserializationTesting(instance, data):
    if (instance.rssi_mode == 1):
        RC232PacketReceiveTesting.id = data[:3]
        RC232PacketReceiveTesting.timestamp = data[3:20]
        RC232PacketReceiveTesting.content = data[21:-1]
        RC232PacketReceiveTesting.rssi = data[-1:]
    else:

        RC232PacketReceiveTesting.content = data

    return RC232PacketReceiveTesting

def print_packet_received(package):
    print("id: ", package.id)
    print("timestamp: ", package.timestamp)
    print("content: ", package.content)
    print("rssi: ", package.rssi)
