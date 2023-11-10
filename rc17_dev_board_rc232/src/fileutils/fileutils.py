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
