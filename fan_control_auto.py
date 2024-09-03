import os
import gpiozero
import psutil
import time

# Configuration (modifiable)
fan_pin = 14  # GPIO pin connected to the fan

# Mode Configuration
target_temp = 50  # Target temperature (Celsius) for automatic mode (Default: 50°C)
temp_tolerance = 4  # Temperature tolerance range (Default: 4°C)

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

def calculate_automatic_fan_speed(temp):
    """Function to calculate the fan speed in automatic mode based on temperature."""
    lower_bound = target_temp - temp_tolerance
    upper_bound = target_temp + temp_tolerance

    if temp <= lower_bound:
        return 0  # Fan at 0% speed when temp is at or below the lower bound
    elif temp >= upper_bound:
        return 100  # Fan at 100% speed when temp is at or above the upper bound
    else:
        # Gradually increase fan speed between the lower and upper bounds
        return int(100 * ((temp - lower_bound) / (upper_bound - lower_bound)))

def main():
    # Set pin 14 to LOW at the start
    fan.off()
    clear_screen()  # Clear screen at the start of the script
    try:
        while True:
            temp = get_cpu_temperature()
            fan_speed_percentage = calculate_automatic_fan_speed(temp)
            
            # Clear screen after each temperature reading
            clear_screen()

            # Display updated temperature and fan speed
            fan.value = fan_speed_percentage / 100  # Convert percentage to 0-1 range for PWM
            fan_speed_display = f"{fan_speed_percentage:3d}%"
            print(f"\rCPU Temp: {temp:.2f}°C, Fan speed: {fan_speed_display}", end='', flush=True)
            
            time.sleep(1)  # Check the temperature every 1 second
    except KeyboardInterrupt:
        pass  # Handle exit with KeyboardInterrupt
    finally:
        # Ensure pin 14 is set to HIGH on exit and clear the screen
        fan.on()  # This will set the pin to HIGH
        clear_screen()  # Clear the screen at the end of the script

if __name__ == "__main__":
    main()
