import RPi.GPIO as GPIO
import time

buzzer_pin = 18
switch_pin = 22

GPIO.setmode(GPIO.BCM)
GPIO.setup(buzzer_pin, GPIO.OUT)
GPIO.setup(switch_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

buzzer_on = False
switch_initial_state = GPIO.input(switch_pin)


def reset_buzzer():
    global buzzer_on
    buzzer_on = True
    GPIO.output(buzzer_pin, GPIO.HIGH)  # buzzer ON

    try:
        # Wait for switch press
        while GPIO.input(switch_pin) == switch_initial_state:
            time.sleep(0.1)

        # Turn off buzzer
        GPIO.output(buzzer_pin, GPIO.LOW)
        buzzer_on = False

    except KeyboardInterrupt:
        pass