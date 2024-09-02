#!/usr/bin/env python3

import time
import sys
import os

def get_temp():
    with open("/sys/class/thermal/thermal_zone0/temp") as f:
        return int(f.read().strip()) / 1000.0

if __name__ == "__main__":
    try:
        while True:
            temp = get_temp()
            os.system('clear')
            sys.stdout.write(f"CPU Temp: {temp:.1f} °C\n")
            sys.stdout.flush()
            time.sleep(1)
    except KeyboardInterrupt:
        sys.stdout.write("\n")
