from hal import hal_led as led

def control_led(on: bool):
    led.init()
    led.set_output(24,on)
    return


    