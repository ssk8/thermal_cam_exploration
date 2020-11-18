#this only kinda works

import busio
import board
import numpy as np
from scipy.interpolate import griddata
import io
import matplotlib.pyplot as plt
from copy import deepcopy 
import adafruit_amg88xx
from PIL import Image
from ST7789 import ST7789

points = [(l,m) for l in range(8) for m in range(8)]
grid = tuple(np.mgrid[0:7:32j, 0:7:32j])
 
i2c_bus = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_amg88xx.AMG88XX(i2c_bus)

lcd = ST7789()
lcd.Init()
lcd.clear()

while not lcd.buttonB:
    sensor_array = np.array(sensor.pixels).ravel()
    bicubic = griddata(points, sensor_array, grid, method='cubic')
    fig, ax = plt.subplots()
    im = ax.imshow(bicubic)
    plt.tick_params(which='both', left=False, labelleft=False, bottom=False, top=False, labelbottom=False)
    buf = io.BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight',pad_inches=0)
    buf.seek(0)
    pil_img = deepcopy(Image.open(buf)).resize([240, 240])
    buf.close()
    lcd.image(pil_img)

lcd.clear()
lcd.backlight(False)