import time
import board
import digitalio
import os
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306
import gpiozero
import psutil

# Configuration for fan control
fan_pin = 14            # GPIO pin connected to the fan
target_temp = 50        # Target temperature (Celsius) for automatic mode
temp_tolerance = 4      # Temperature tolerance range

# Configuration for refresh interval
refresh_interval = 1.0  # Intervalul de refresh al display-ului (în secunde)

# Configuration for display
text_x_large = 0        # X-coordinate for large text (temperature) 0
text_y_large = 5        # Y-coordinate for large text (temperature) 5
text_x_small_target = 80 # X-coordinate for small text (target temperature) 80
text_y_small_target = 2  # Y-coordinate for small text (target temperature) 2
text_x_small_fan = 80   # X-coordinate for small text (fan speed) 80
text_y_small_fan = 20   # Y-coordinate for small text (fan speed) 20

# Font configuration
font_large_path = 'PixelGameFont.ttf'  # Path for large font
font_small_path = 'PixelGameFont.ttf'  # Path for small font
font_large_size = 32    # Font size for large text (temperature) 32
font_small_size = 16    # Font size for small text (target temperature and fan speed)

# Initialize the fan control using PWM
fan = gpiozero.PWMOutputDevice(fan_pin)

# Define the Reset Pin for the OLED display
oled_reset = digitalio.DigitalInOut(board.D4)

# Display Parameters
width = 128
height = 32  # Înălțimea display-ului OLED

# Load fonts
font_large = ImageFont.truetype(font_large_path, font_large_size)
font_small = ImageFont.truetype(font_small_path, font_small_size)

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

# Initialize the OLED display
i2c = board.I2C()
oled = adafruit_ssd1306.SSD1306_I2C(width, height, i2c, addr=0x3C, reset=oled_reset)

# Clear display.
oled.fill(0)
oled.show()

# Create blank image for drawing.
image = Image.new("1", (oled.width, oled.height))
draw = ImageDraw.Draw(image)

try:
    while True:
        # Get the current CPU temperature
        temp = get_cpu_temperature()

        # Calculate the fan speed based on the current temperature
        fan_speed_percentage = calculate_automatic_fan_speed(temp)
        
        # Update the fan speed
        fan.value = fan_speed_percentage / 100  # Convert percentage to 0-1 range for PWM

        # Clear the image for display update
        draw.rectangle((0, 0, oled.width, oled.height), outline=0, fill=0)

        # Convert temperature to string with one decimal and display it on the OLED
        temp_str = f"{temp:.1f}"  # Afișează temperatura cu o singură zecimală
        draw.text((text_x_large, text_y_large), temp_str, font=font_large, fill=255)

        # Display target temperature at (80, 2) with font size 16
        target_temp_str = f" {target_temp}°C"
        draw.text((text_x_small_target, text_y_small_target), target_temp_str, font=font_small, fill=255)

        # Display fan speed at (80, 20) with font size 16
        fan_speed_str = f" {fan_speed_percentage:2d}%"
        draw.text((text_x_small_fan, text_y_small_fan), fan_speed_str, font=font_small, fill=255)

        # Update the OLED display with the new image
        oled.image(image)
        oled.show()

        # Display updated temperature and fan speed on the terminal
        fan_speed_display = f"{fan_speed_percentage:3d}%"
        clear_screen()
        print(f"\rCPU Temp: {temp:.1f} °C, Fan speed: {fan_speed_display}", end='', flush=True)

        # Wait before the next update
        time.sleep(refresh_interval)

except KeyboardInterrupt:
    pass  # Handle exit with KeyboardInterrupt
finally:
    # Ensure fan is turned on before exiting
    fan.on()  # This will set the fan to full speed
    clear_screen()  # Clear the terminal screen
    # Clear the OLED display
    draw.rectangle((0, 0, oled.width, oled.height), outline=0, fill=0)
    oled.image(image)
    oled.show()
