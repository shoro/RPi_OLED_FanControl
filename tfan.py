#!/usr/bin/env python3

# Version: 1.1.7

import time
import sys
import os
import RPi.GPIO as GPIO

# GPIO pin configuration
FAN_PIN = 14  # GPIO pin connected to the relay or transistor controlling the fan
TEMP_ON = 60.0
TEMP_OFF = 50.0

def setup_gpio():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(FAN_PIN, GPIO.OUT)
    GPIO.output(FAN_PIN, GPIO.LOW)  # Ensure fan is off initially

def get_temp():
    with open("/sys/class/thermal/thermal_zone0/temp") as f:
        return int(f.read().strip()) / 1000.0

def control_fan(temp):
    if temp >= TEMP_ON:
        GPIO.output(FAN_PIN, GPIO.HIGH)  # Turn on the fan
    elif temp <= TEMP_OFF:
        GPIO.output(FAN_PIN, GPIO.LOW)   # Turn off the fan

if __name__ == "__main__":
    try:
        setup_gpio()
        while True:
            temp = get_temp()
            os.system('clear')  # Clear the terminal screen
            control_fan(temp)
            sys.stdout.write(f"CPU Temp: {temp:.1f} °C\n")
            sys.stdout.flush()
            time.sleep(1)
    except KeyboardInterrupt:
        GPIO.cleanup()  # Clean up GPIO on exit
        sys.stdout.write("\n")
