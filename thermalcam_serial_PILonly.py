import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import griddata
import serial
from PIL import Image
from colour import Color


MINTEMP = 18
MAXTEMP = 32

points = [(l,m) for l in range(8) for m in range(8)]
grid = tuple(np.mgrid[0:7:32j, 0:7:32j])

colors = list(Color("indigo").range_to(Color("red"), 255))
colors = [(int(c.red * 255), int(c.green * 255), int(c.blue * 255)) for c in colors]

def map_value(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def constrain(val, min_val, max_val):
    return min(max_val, max(min_val, val))


pil_img = Image.new('RGB', [32,32], 255)
if True:
    with serial.Serial('/dev/ttyACM0') as ser:
        ser_bytes = ser.readline()

    pixels = map_value(np.array([float(p) for p in ser_bytes.split()]), MINTEMP, MAXTEMP, 0, 254)
    bicubic = griddata(points, pixels, grid, method='cubic')
   

    data = pil_img.load()

    for ix, row in enumerate(bicubic):
        for jx, pixel in enumerate(row):
            data[ix, jx] = colors[constrain(int(pixel), 0, 254)]
 

    pil_img = pil_img.resize((240, 240))
    pil_img.show()
