# Created by: Peter Burdohan
# Based on original python script made by Michael Klements: https://github.com/mklements/OLED_Stats.git
# For Raspberry Pi 4B Desktop with OLED Stats Display
# Base on Adafruit CircuitPython & SSD1306 Libraries

import time
import board
import busio
import digitalio

from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306

import subprocess

# Define the Reset Pin
oled_reset = digitalio.DigitalInOut(board.D4)

# Display Parameters
WIDTH = 128
HEIGHT = 64
BORDER = 5

# Use for I2C.
i2c = board.I2C()
oled = adafruit_ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c, addr=0x3C, reset=oled_reset)

# Clear display.
oled.fill(0)
oled.show()

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
image = Image.new("1", (oled.width, oled.height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a white background
draw.rectangle((0, 0, oled.width, oled.height), outline=255, fill=255)

cmd = "whoami"
user = str(subprocess.check_output(cmd, shell = True ), "utf-8").replace('\n','')
font = ImageFont.truetype('/home/'+user+'/rpi_oled_display_stat/open_24_display_st.ttf', 15)
#font = ImageFont.load_default()

while True:

    # Draw a black filled box to clear the image.
    draw.rectangle((0, 0, oled.width, oled.height), outline=0, fill=0)

    # Shell scripts for system monitoring from here : https://unix.stackexchange.com/questions/119126/command-to-display-memory-usage-disk-usage-and-cpu-load
    cmd = "hostname -I | cut -d\' \' -f1"
    IP = subprocess.check_output(cmd, shell = True )
    cmd = "date +%R" 
    cur_time = subprocess.check_output(cmd, shell = True )
    cmd = "top -bn1 | grep load | awk '{printf \"CPU: %d\", $(NF-2)}'"
    CPU = subprocess.check_output(cmd, shell = True )
    cmd = "free -m | awk 'NR==2{printf \"RAM: %.2f/%.2fGB %d%%\", $3/1024,$2/1024,$3*100/$2 }'"
    MemUsage = subprocess.check_output(cmd, shell = True )
    cmd = "df -h | awk '$NF==\"/\"{printf \"SSD: %d/%dGB %s\", $3,$2,$5}'"
    Disk = subprocess.check_output(cmd, shell = True )
    cmd = "vcgencmd measure_temp |cut -f 2 -d '=' | sed -e 's/\..*/°C/'"
    temp = subprocess.check_output(cmd, shell = True )

    # Pi Stats Display
    draw.text((0, 0), str(IP,'utf-8'), font=font, fill=255)
    draw.text((97, 0), str(cur_time,'utf-8'), font=font, fill=255)
    draw.text((0, 16), str(CPU,'utf-8') + "%", font=font, fill=255)
    draw.text((60, 16), "TEMP: " + str(temp,'utf-8'), font=font, fill=255)
    draw.text((0, 32), str(MemUsage,'utf-8'), font=font, fill=255)
    draw.text((0, 48), str(Disk,'utf-8'), font=font, fill=255)
        
    # Display image
    oled.image(image)
    oled.show()
    time.sleep(.1)
