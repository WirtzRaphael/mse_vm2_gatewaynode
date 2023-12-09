import random
import rc232.testing
import timeutil.timeutil

def get_test_string():
    return "Hello, device!"
    
def get_test_data_set_send():
    testset = []
    time_now = timeutil.timeutil.get_time_utc()
    sample_rate = 1
    for i in range(1, 11):
        value_16bit = bin(random.randrange(65536))[2:].zfill(16)
        packet = rc232.testing.RC232PacketSendTesting(
            id=f"{i:03}",
            timestamp=time_now + i * sample_rate,
            content=value_16bit
        )
        testset.append(packet)
    return testset
