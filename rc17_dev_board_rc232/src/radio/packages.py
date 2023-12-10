

PAYLOAD_SEPARATOR = '-'
PACKAGE_END_CHAR = ';'
RC_232_PACKET_END_CHAR = 'LF'

def split_into_packages(package_stream):
    if package_stream == "":
        return
    packet_list = package_stream.split(PACKAGE_END_CHAR)
    return packet_list

def payload_readout(package):
    payload_list = package.split(PAYLOAD_SEPARATOR)
    # fix : magic number
    if payload_list == None or len(payload_list) <= 2:
        return
    
    payload = ProtocolPayload(
        timestampRtc=payload_list[0],
        sensor_nr=payload_list[1]
    )
    
    # fix : magic number
    for x in range(2, len(payload_list),2):
        #print("payload_list 0: ", payload_list[x])
        #print("payload_list 1: ", payload_list[x+1])
        payload.add_payload_temperature(payload_list[x], payload_list[x+1])
        pass # no content, avoid error
    return payload


# todo : remove
def deserialization_sensor(package):
    payload_list = package.split(PAYLOAD_SEPARATOR)
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
    

def print_package_received_sensor(package):
    print("temperature1: ", package.temperature1)
    print("temperature1 Id: ", package.temperatureId1)
    print("temperature2: ", package.temperature2)
    print("temperature2 Id: ", package.temperatureId2)


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

class ProtocolPayload:
    def __init__(self, sensor_nr, timestampRtc) -> None:
        self.sensor_nr = sensor_nr
        self.timestampRtc = timestampRtc
        self.sensorTemperatureValues = []
    
    def add_payload_temperature(self, temperature, sensorId):
        sensorTemperature = _PayloadTemperature(temperature, sensorId)
        self.sensorTemperatureValues.append(sensorTemperature)

    def print_payload(self):
        print("Payload: ")
        for sensorTemperature in self.sensorTemperatureValues:
            print("SensorId: ", sensorTemperature.temperatureId)
            print("Temperature: ", sensorTemperature.temperature)

class _PayloadTemperature:
    def __init__(self, temperature, temperatureId):
        self.temperature = temperature
        self.temperatureId = temperatureId
