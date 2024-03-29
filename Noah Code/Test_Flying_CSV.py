from __future__ import print_function

from dronekit import connect, VehicleMode, LocationGlobalRelative, LocationGlobal, Command
import time
import math
from pymavlink import mavutil
import csv

#Set up option parsing to get connection string
import argparse  
parser = argparse.ArgumentParser(description='Demonstrates basic mission operations.')
parser.add_argument('--connect', 
                   help="vehicle connection target string. If not specified, SITL automatically started and used.")
args = parser.parse_args()

connection_string = args.connect
sitl = None


#Start SITL if no connection string specified
if not connection_string:
    import dronekit_sitl
    sitl = dronekit_sitl.start_default()
    connection_string = sitl.connection_string()


# Connect to the Vehicle
print('Connecting to vehicle on: %s' % connection_string)
vehicle = connect(connection_string, wait_ready=True)

def arm_and_takeoff(aTargetAltitude):
    """
    Arms vehicle and fly to aTargetAltitude.
    """

    print("Basic pre-arm checks")
    # Don't let the user try to arm until autopilot is ready
    while not vehicle.is_armable:
        print(" Waiting for vehicle to initialise...")
        time.sleep(1)

        
    print("Arming motors")
    # Copter should arm in GUIDED mode
    vehicle.mode = VehicleMode("GUIDED")
    vehicle.armed = True

    while not vehicle.armed:      
        print(" Waiting for arming...")
        time.sleep(1)

    print("Taking off!")
    vehicle.simple_takeoff(aTargetAltitude) # Take off to target altitude

    # Wait until the vehicle reaches a safe height before processing the goto (otherwise the command 
    #  after Vehicle.simple_takeoff will execute immediately).
    while True:
        print(" Altitude: ", vehicle.location.global_relative_frame.alt)      
        if vehicle.location.global_relative_frame.alt>=aTargetAltitude*0.95: #Trigger just below target alt.
            print("Reached target altitude")
            break
        time.sleep(1)

home = [vehicle.location.global_frame.lat, vehicle.location.global_frame.lon, vehicle.location.global_frame.alt]

arm_and_takeoff(10)
vehicle.mode = VehicleMode("GUIDED")

header = []
rows = []
#leader = open('Leader_Position.csv')
#type(file)

fieldnames = ['lat', 'long', 'alt', 'time']

delay = 1

x = 0
y = 0
z = 0
t = 0

with open('Follower_Position.csv', 'w') as csv_file:
    csv_writer = csv.DictWriter(csv_file, fieldnames = fieldnames)
    csv_writer.writeheader()

with open('Follower_Plot.csv', 'w') as csv_file:
    csv_writer2 = csv.DictWriter(csv_file, fieldnames = fieldnames)
    csv_writer2.writeheader()

leader = open('Leader_Plot.csv')
type(leader)
    
while True:
    vehicle.mode = VehicleMode("GUIDED")
    csvreader = csv.reader(leader)
    #header = next(csvreader)
    for row in csvreader:
        rows.append(row)

    location = (rows[-1])

    point = LocationGlobalRelative(float(location[0]), float(location[1]), float(location[2]))

    print(point)

    vehicle.simple_goto(point, groundspeed=3)

    with open('Follower_Position.csv', 'a') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        info = {
            'lat':x,
            'long':y,
            'alt':z,
            'time':t
        }

        csv_writer.writerow(info)
        #print(x, y, z, t)
        t += delay
        x = vehicle.location.global_frame.lat #scaling to get "readable values"
        y = vehicle.location.global_frame.lon
        z = vehicle.location.global_frame.alt - home[2]


    with open('Follower_Plot.csv', 'a') as csv_file:
        csv_writer2 = csv.DictWriter(csv_file, fieldnames=fieldnames)

        info = {
            'lat':x,
            'long':y,
            'alt':z,
            'time':t
        }

        csv_writer2.writerow(info)
        #print(x, y, z, t)
        t += delay
        x = (vehicle.location.global_frame.lat - home[0])*1e4 #scaling to get "readable values"
        y = (vehicle.location.global_frame.lon - home[1])*1e4
        z = vehicle.location.global_frame.alt - home[2]

    time.sleep(0.1)

file.close()