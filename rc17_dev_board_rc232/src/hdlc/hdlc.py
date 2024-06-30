


def hdlc_decode(data):
    frames = []
    frame = []
    escape = False
    in_frame = False

    for byte in data:
        if byte == 0x7E:  # Flag sequence
            if in_frame and frame:
                frames.append(bytes(frame))
                frame = []
            in_frame = not in_frame
            continue

        if in_frame:
            if byte == 0x7D:  # Escape character
                escape = True
                continue
            if escape:
                byte ^= 0x20
                escape = False
            frame.append(byte)

    return frames