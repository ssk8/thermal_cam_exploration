import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import griddata
import serial
from PIL import Image
from colour import Color
import busio
import board
import numpy as np
import adafruit_amg88xx
from ST7789 import ST7789


MINTEMP = 18
MAXTEMP = 32

points = [(l,m) for l in range(8) for m in range(8)]
grid = tuple(np.mgrid[0:7:32j, 0:7:32j])

colors = list(Color("indigo").range_to(Color("red"), 255))
colors = [(int(c.red * 255), int(c.green * 255), int(c.blue * 255)) for c in colors]

def map_value(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

i2c_bus = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_amg88xx.AMG88XX(i2c_bus)

lcd = ST7789()
lcd.Init()
lcd.clear()

while not lcd.buttonA:
    sensor_values = np.rot90(np.array(sensor.pixels))
    pixels = map_value(sensor_values.ravel(), MINTEMP, MAXTEMP, 0, 254)
    bicubic = griddata(points, pixels, grid, method='cubic')
   
    pil_img = Image.new('RGB', [32,32], 255)
    data = pil_img.load()

    for ix, row in enumerate(bicubic):
        for jx, pixel in enumerate(row):
            data[ix, jx] = colors[min(254, max(0, int(pixel)))]

    lcd.image(pil_img.resize((240, 240)))
    while lcd.buttonB:
        pass #pause image

lcd.clear()
lcd.backlight(False)
