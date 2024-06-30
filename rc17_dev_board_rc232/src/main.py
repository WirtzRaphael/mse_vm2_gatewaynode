import sys
import apps.mode_gateway_pc
import apps.mode_gateway_pc_v2
import apps.mode_performance_testing

# param
#OPERATION_MODE = sys.argv[1] # gateway_pc, gateway_pi4, performance_testing 
#SERIAL_PORT_RC_DEVBOAD = sys.argv[2] # '/dev/ttyUSB0'

# default
#OPERATION_MODE = 'gateway_pc' 
OPERATION_MODE = 'gateway_pc_v2' 

SERIAL_PORT_RC_DEVBOARD = '/dev/ttyUSB0'

def run_mode_gateway_pi4():
    return

if __name__ == "__main__":
    while(True):
        match OPERATION_MODE:
            case 'gateway_pc_v2':
                apps.mode_gateway_pc_v2.run_mode_gateway_pc_v2(OPERATION_MODE, SERIAL_PORT_RC_DEVBOARD, True)
            case 'gateway_pi4':
                print("MODE: raspberry pi \n")
                run_mode_gateway_pi4()
                # todo : v2 pc receive
            case _:
                print("no mode\n")

