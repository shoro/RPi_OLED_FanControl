import time
import board
import busio
import digitalio
import subprocess
import os
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306
import RPi.GPIO as GPIO  # Import GPIO library

# Configuration
# --------------------
TEMP_OFF = 50.0       # Temperatura de prag pentru oprirea ventilatorului (°C)
TEMP_ON = 60.0        # Temperatura de prag pentru activarea ventilatorului (°C)
FAN_PIN = 14          # Pinul GPIO la care este conectat ventilatorul (GPIO14)
REFRESH_INTERVAL = 1.0 # Intervalul de refresh al display-ului (în secunde)
FONT_SIZE = 32        # Dimensiunea fontului (în pixeli)
TEXT_X = 18           # Coordonata X a textului pe display
TEXT_Y = 1            # Coordonata Y a textului pe display

# Initialize GPIO
GPIO.setmode(GPIO.BCM)  # Set GPIO mode to BCM
GPIO.setup(FAN_PIN, GPIO.OUT)  # Set FAN_PIN as an output

# Define the Reset Pin and Fan Control Pin
oled_reset = digitalio.DigitalInOut(board.D4)
fan_pin = FAN_PIN

# Display Parameters
WIDTH = 128
HEIGHT = 32  # Înălțimea display-ului OLED

# Clear terminal screen at the beginning
os.system('clear')  # For Linux/Mac
# os.system('cls')  # Uncomment this line for Windows

# Initialize fan pin to LOW
GPIO.output(fan_pin, GPIO.LOW)  # Set pin to LOW initially

# Use for I2C.
i2c = board.I2C()
oled = adafruit_ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c, addr=0x3C, reset=oled_reset)

# Clear display.
oled.fill(0)
oled.show()

# Create blank image for drawing.
image = Image.new("1", (oled.width, oled.height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Load font
font = ImageFont.truetype('PixelOperator.ttf', FONT_SIZE)  # Use PixelOperator.ttf with FONT_SIZE

try:
    while True:
        # Clear the image.
        draw.rectangle((0, 0, oled.width, oled.height), outline=0, fill=0)

        # Get temperature
        cmd = "vcgencmd measure_temp | cut -f 2 -d '='"
        Temp = subprocess.check_output(cmd, shell=True)
        Temp = Temp.decode('utf-8').strip()  # Decode and remove any trailing newline

        # Remove 'C' and keep only '°C'
        if Temp.endswith("'C"):  
            Temp = Temp[:-2] + " °C"  # Add a space before '°C'
            
        # Extract temperature value for control logic
        temp_value = float(Temp[:-3])  # Convert to float, remove '°C'

        # Control the fan based on temperature
        if temp_value >= TEMP_ON:
            GPIO.output(fan_pin, GPIO.HIGH)  # Turn on the fan
        elif temp_value <= TEMP_OFF:
            GPIO.output(fan_pin, GPIO.LOW)  # Turn off the fan

        # Display temperature at the defined position
        draw.text((TEXT_X, TEXT_Y), Temp, font=font, fill=255)

        # Update OLED display
        oled.image(image)
        oled.show()

        # Wait before next update
        time.sleep(REFRESH_INTERVAL)

except KeyboardInterrupt:
    # Ensure the fan is turned on before exiting
    GPIO.output(fan_pin, GPIO.HIGH)  # Set pin to HIGH to keep the fan on

    # Clear the OLED display
    draw.rectangle((0, 0, oled.width, oled.height), outline=0, fill=0)
    oled.image(image)
    oled.show()

    # Clear terminal screen on exit
    os.system('clear')  # For Linux/Mac
    # os.system('cls')  # Uncomment this line for Windows

    # Cleanup GPIO settings
    GPIO.cleanup()
