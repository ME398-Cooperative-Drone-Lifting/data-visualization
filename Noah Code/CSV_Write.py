from __future__ import print_function
from dronekit import connect, VehicleMode, LocationGlobalRelative, LocationGlobal, Command
import time
import math
from pymavlink import mavutil
import dronekit_sitl
import csv


fieldnames = ['lat', 'long', 'alt', 'time']

delay = 1
x = 0
y = 0
z = 0
t = 0

with open('test.csv', 'w') as csv_file:
    csv_writer = csv.DictWriter(csv_file, fieldnames = fieldnames)
    csv_writer.writeheader()

for i in range(50):
    with open('test.csv', 'a') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        info = {
        'lat':x,
        'long':y,
        'alt':z,
        'time':t
        }

        print(x, y, z, t)
        print(i)
        csv_writer.writerow(info)
        t += delay
        x = 40.0 + i*2
        y = 60.0 + i
        z = 10.0 

        time.sleep(3)