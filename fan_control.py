import os
import gpiozero
import psutil
import time

# Configuration (modifiable)
fan_pin = 14  # GPIO pin connected to the fan
start_temp = 40  # Start temperature (Celsius) for the fan to begin increasing speed
max_temp = 60  # Maximum temperature (Celsius) at which the fan reaches max speed
start_fan_speed = 10  # Fan speed (%) at the start temperature (0-100)
max_fan_speed = 100  # Fan speed (%) at the maximum temperature (0-100)

# Set up PWM on the fan pin
fan = gpiozero.PWMOutputDevice(fan_pin)

def clear_screen():
    """Function to clear the terminal screen."""
    os.system('clear')

def get_cpu_temperature():
    """Function to return the CPU temperature in Celsius."""
    temps = psutil.sensors_temperatures()
    if 'cpu_thermal' in temps:
        return temps['cpu_thermal'][0].current
    else:
        raise RuntimeError("CPU temperature sensor not found.")

def calculate_fan_speed(temp):
    """Function to calculate the fan speed based on the temperature."""
    if temp < start_temp:
        return start_fan_speed  # Fan speed at temperatures below start_temp
    elif start_temp <= temp < max_temp:
        return start_fan_speed + (max_fan_speed - start_fan_speed) * ((temp - start_temp) / (max_temp - start_temp))  # Gradual increase
    else:
        return max_fan_speed  # Max fan speed at temperatures above max_temp

def main():
    clear_screen()  # Clear screen at the start of the script
    try:
        while True:
            temp = get_cpu_temperature()
            fan_speed_percentage = calculate_fan_speed(temp)
            fan.value = fan_speed_percentage / 100  # Convert percentage to 0-1 range for PWM
            print(f"\rTemperature: {temp:.1f}°C, Fan speed: {fan_speed_percentage:.1f}%", end='', flush=True)
            time.sleep(1)  # Check the temperature every 1 second
    except KeyboardInterrupt:
        clear_screen()  # Clear screen at the end of the script without additional messages

if __name__ == "__main__":
    main()
