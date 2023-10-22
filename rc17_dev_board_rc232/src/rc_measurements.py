from datetime import timezone 
import datetime 
import random
import rc232

def get_test_string():
    return "Hello, device!"
    
def get_test_data_set_send():
    testset = []
    time_now = get_time_utc(datetime.datetime.now())
    sample_rate = 5
    for i in range(1, 5):
        value_16bit = bin(random.randrange(65536))[2:].zfill(16)
        packet = rc232.RC232PacketSend(
            id=f"{i:03}",
            timestamp=time_now + i * sample_rate,
            content=value_16bit
        )
        testset.append(packet)
    return testset

def get_time_utc(datetime):
    utc_time = datetime.replace(tzinfo=timezone.utc) 
    utc_timestamp = utc_time.timestamp()
    return utc_timestamp

def get_time_iso(datetime):
    iso_timestamp_str = datetime.isoformat()
    return iso_timestamp_str

def convert_time_utc_to_iso(utc_timestamp):
    utc_datetime = datetime.datetime.fromtimestamp(utc_timestamp, timezone.utc)
    iso_timestamp_str = utc_datetime.isoformat()
    return iso_timestamp_str

def write_to_file(rc232_packets, filename):
    separator = ';'
    with open(filename, "w") as file:
        for packet in rc232_packets:
            packet_str = f"{packet.id},{packet.timestamp},{packet.content}{separator}\n"
            file.write(packet_str)

def append_to_file(rc232_packet, filename):
    with open(filename, "a") as file:
        separator = ';'
        packet_str = f"{rc232_packet.id},{rc232_packet.timestamp},{rc232_packet.content},{rc232_packet.rssi}{separator}\n"
        file.write(packet_str)
