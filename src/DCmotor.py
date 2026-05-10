import RPi.GPIO as GPIO
import time

motor_pin = 23


def spin_motor(items: list):

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(motor_pin, GPIO.OUT)
    spin_duration = len(items)
    GPIO.output(motor_pin, GPIO.HIGH)
    time.sleep(spin_duration)
    GPIO.output(motor_pin, GPIO.LOW)
    GPIO.cleanup()