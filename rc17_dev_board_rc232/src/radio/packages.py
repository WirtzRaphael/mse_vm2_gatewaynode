PAYLOAD_SEPARATOR = '-'
PACKAGE_END_CHAR = ';'
RC_232_PACKET_END_CHAR = 'LF'

PAYLOAD_INDEX_TIMESTAMP_RTC = 1
PAYLOAD_INDEX_SENSOR_NR = 2
PAYLOAD_INDEX_SENSOR_TEMPERATURE = 3

PAYLOAD_LENGTH_TEMPERATURE = 2

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

def split_into_packages(package_stream):
    if package_stream == "":
        return
    packet_list = package_stream.split(PACKAGE_END_CHAR)
    return packet_list

def payload_readout(package) -> ProtocolPayload:
    payload_content_list = package.split(PAYLOAD_SEPARATOR)
    # fix : magic number
    if payload_content_list == None or len(payload_content_list) <= 2:
        return
    try:
        payload_index_start_temperature = payload_content_list.index('T')
    except ValueError:
        # fix : Line Feed (LF) at payload start
        try:
            payload_index_start_temperature = payload_content_list.index('LFT')
        except ValueError:
            return None
    
    payload = ProtocolPayload(
        timestampRtc=payload_content_list[payload_index_start_temperature + PAYLOAD_INDEX_TIMESTAMP_RTC],
        sensor_nr=payload_content_list[payload_index_start_temperature + PAYLOAD_INDEX_SENSOR_NR]
    )
    
    for x in range(payload_index_start_temperature + PAYLOAD_INDEX_SENSOR_TEMPERATURE, len(payload_content_list), payload_index_start_temperature + PAYLOAD_LENGTH_TEMPERATURE):
        try:
            #print("payload_list 0: ", payload_list[x])
            #print("payload_list 1: ", payload_list[x+1])
            payload.add_payload_temperature(payload_content_list[x], payload_content_list[x+1])
        except IndexError:
            # index out of bounds, corrupt or incomplete values
            pass
        pass # no content, avoid error
    return payload

def print_package_received_sensor(package):
    print("temperature1: ", package.temperature1)
    print("temperature1 Id: ", package.temperatureId1)
    print("temperature2: ", package.temperature2)
    print("temperature2 Id: ", package.temperatureId2)


