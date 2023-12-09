import mode_gateway_pc
import mode_performance_testing

def run_mode_gateway_pi4():
    return

operation_mode = 'gateway_pc'

if __name__ == "__main__":
    while(True):
        match operation_mode:
            case 'gateway_pc':
                with mode_gateway_pc.mode_gateway_pc():
                    while(operation_mode == operation_mode{mode_gateway_pc}}):
                        mode_gateway_pc.run_mode_gateway_pc()
            case 'gateway_pi4':
                print("MODE: raspberry pi \n")
                run_mode_gateway_pi4()
            case 'performance_testing':
                print("MODE: performance testing \n")
                mode_performance_testing.run_mode_performance_testing()
            case _:
                print("no mode\n")

