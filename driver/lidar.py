# SPDX-FileCopyrightText: 2019 Dave Astels for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""
Consume LIDAR measurement file and create an image for display.

Adafruit invests time and resources providing this open source code.
Please support Adafruit and open source hardware by purchasing
products from Adafruit!

Written by Dave Astels for Adafruit Industries
Copyright (c) 2019 Adafruit Industries
Licensed under the MIT license.

All text above must be included in any redistribution.
"""
import socketio
import os
from math import cos, sin, pi, floor
import pygame
from adafruit_rplidar import RPLidar
import time

sio = socketio.Client()

# Set up pygame and the display
os.putenv('SDL_FBDEV', '/dev/fb1')
pygame.init()
lcd = pygame.display.set_mode((320, 240))
pygame.mouse.set_visible(False)
lcd.fill((0, 0, 0))
pygame.display.update()

# Setup the RPLidar
PORT_NAME = "/dev/ttyS0"
lidar = RPLidar(None, PORT_NAME)

# used to scale data to fit on the screen
max_distance = 0

# pylint: disable=redefined-outer-name,global-statement


def process_data(data):
    global max_distance
    lcd.fill((0, 0, 0))
    data = []
    for angle in range(360):
        distance = data[angle]
        if distance > 0:                  # ignore initially ungathered data points
            max_distance = max([min([5000, distance]), max_distance])
            radians = angle * pi / 180.0
            x = distance * cos(radians)
            y = distance * sin(radians)
            point = (160 + int(x / max_distance * 119),
                     120 + int(y / max_distance * 119))
            data.append(point)
            lcd.set_at(point, pygame.Color(255, 255, 255))
    pygame.display.update()
    return data


scan_data = [0]*360

sio.connect('http://10.13.82.169:3000')
sio.wait()

try:
    print("STUFF IN SOCKET")

    @sio.event
    def connect():
        print('connection established')
        sio.emit("ID", 'RescueRover')
        print(lidar.info)

        while (True):
            for scan in lidar.iter_scans():
                for (_, angle, distance) in scan:
                    scan_data[min([359, floor(angle)])] = distance
                cart = process_data(scan_data)
                sio.emit("lidar", cart)

    @sio.event
    def disconnect():
        print('disconnected from server')

except KeyboardInterrupt:
    time.sleep(0.2)
