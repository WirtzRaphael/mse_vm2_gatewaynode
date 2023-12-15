import sys
import mode_gateway_pc
import mode_performance_testing

# param
#OPERATION_MODE = sys.argv[1] # gateway_pc, gateway_pi4, performance_testing 
#SERIAL_PORT_RC_DEVBOAD = sys.argv[2] # '/dev/ttyUSB0'

# default
OPERATION_MODE = 'gateway_pc' 
SERIAL_PORT_RC_DEVBOAD = '/dev/ttyUSB0'

def run_mode_gateway_pi4():
    return

if __name__ == "__main__":
    while(True):
        match OPERATION_MODE:
            case 'gateway_pc':
                mode_gateway_pc.run_mode_gateway_pc(OPERATION_MODE, SERIAL_PORT_RC_DEVBOAD)
            case 'gateway_pi4':
                print("MODE: raspberry pi \n")
                run_mode_gateway_pi4()
            case 'performance_testing':
                print("MODE: performance testing \n")
                mode_performance_testing.run_mode_performance_testing()
            case _:
                print("no mode\n")

