from __future__ import print_function
from dronekit import connect, VehicleMode, LocationGlobalRelative, LocationGlobal, Command
import time
import math
from pymavlink import mavutil
import dronekit_sitl
import csv
import os

File1 = 'mission_basic.csv'
File2 = 'out.csv'

with open(File1, "r") as r, open(File2, "w+") as w: 
     reader = csv.reader(r, lineterminator = "\n")
     writer = csv.writer(w, lineterminator = "\n")

     for counter,row in enumerate(reader):
         print(row)
         if counter<0: continue
         #if counter>50:break
         writer.writerow(row)
         time.sleep(2)