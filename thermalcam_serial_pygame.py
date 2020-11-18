import os
import numpy as np
import pygame
from scipy.interpolate import griddata
import serial 
from colour import Color
 
MINTEMP = 18.
MAXTEMP = 32.
 
COLORDEPTH = 1024
 
os.putenv('SDL_FBDEV', '/dev/fb1')
pygame.init()
 
points = [(l,m) for l in range(8) for m in range(8)]
grid = tuple(np.mgrid[0:7:32j, 0:7:32j])

colors = list(Color("indigo").range_to(Color("red"), 255))
colors = [(int(c.red * 255), int(c.green * 255), int(c.blue * 255)) for c in colors]
 
height = 240
width = 240
 
displayPixelWidth = width / 30
displayPixelHeight = height / 30
 
lcd = pygame.display.set_mode((width, height))
 
lcd.fill((255, 0, 0))
 
pygame.display.update()
pygame.mouse.set_visible(False)
 
lcd.fill((0, 0, 0))
pygame.display.update()
 
def constrain(val, min_val, max_val):
    return min(max_val, max(min_val, val))
 
def map_value(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
 
while True:
    with serial.Serial('/dev/ttyACM0') as ser:
        ser_bytes = ser.readline()
    pixels = map_value(np.array([float(p) for p in ser_bytes.split()]), MINTEMP, MAXTEMP, 0, 254)
    bicubic = griddata(points, pixels, grid, method='cubic')
    for ix, row in enumerate(bicubic):
        for jx, pixel in enumerate(row):
            pygame.draw.rect(lcd, colors[constrain(int(pixel), 0, COLORDEPTH- 1)],
                             (displayPixelHeight * ix, displayPixelWidth * jx,
                              displayPixelHeight, displayPixelWidth))
    pygame.display.update()