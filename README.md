# thermal_cam_exploration
just messing around with AMG8833 sensor

All based on adafruit AMG8833 driver and examples. For serial, I used QTPy as I2C interface. Works with delay at 100ms


"thermalcam_to_1.3inch_miniPiTFT.py" works well (better than 1 fps) but could be improved, particularly in the color assignment. This is written for use with the included "ST7789.py" and not the adafruit lcd library but works with the later as well
