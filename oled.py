import time
import board
import busio
import digitalio
import subprocess
import os
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306

# Configuration
# --------------------
REFRESH_INTERVAL = 1.0 # Intervalul de refresh al display-ului (în secunde)
FONT_SIZE = 32        # Dimensiunea fontului (în pixeli)
TEXT_X = 18           # Coordonata X a textului pe display
TEXT_Y = 1            # Coordonata Y a textului pe display

# Define the Reset Pin
oled_reset = digitalio.DigitalInOut(board.D4)

# Display Parameters
WIDTH = 128
HEIGHT = 32  # Înălțimea display-ului OLED

# Clear terminal screen at the beginning
os.system('clear')  # For Linux/Mac
# os.system('cls')  # Uncomment this line for Windows

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
            
        # Display temperature at the defined position
        draw.text((TEXT_X, TEXT_Y), Temp, font=font, fill=255)

        # Update OLED display
        oled.image(image)
        oled.show()

        # Wait before next update
        time.sleep(REFRESH_INTERVAL)

except KeyboardInterrupt:
    # Clear the OLED display
    draw.rectangle((0, 0, oled.width, oled.height), outline=0, fill=0)
    oled.image(image)
    oled.show()

    # Clear terminal screen on exit
    os.system('clear')  # For Linux/Mac
    # os.system('cls')  # Uncomment this line for Windows
