from __future__ import print_function

from dronekit import connect, VehicleMode, LocationGlobalRelative, LocationGlobal, Command
import time
import math
from pymavlink import mavutil
import csv
import pandas as pd

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

# vehicle home location
home = [vehicle.location.global_frame.lat, vehicle.location.global_frame.lon, vehicle.location.global_frame.alt]

arm_and_takeoff(10)
vehicle.mode = VehicleMode("GUIDED")

# reading csv output from leader drone
location_df = pd.read_csv('location.csv')
print(location_df.head())
headers = list(location_df)

altitude_offset = 2
target_x = location_df[headers[0]][0]
target_y = location_df[headers[1]][0]
target_z = location_df[headers[2]][0]

# writing csv for data visualization
delay = 0.1

x = 0
y = 0
z = 0
t = 0

with open('fly_to_point.csv', 'w') as csv_file:
    csv_writer = csv.DictWriter(csv_file, fieldnames = headers)
    csv_writer.writeheader()
    relative_target_loc = {
            'lat':target_x-home[0],
            'long':target_y-home[1],
            'alt':target_z,
            'time':0
        }
    csv_writer.writerow(relative_target_loc)

vehicle.mode = VehicleMode("GUIDED")
point = LocationGlobalRelative(float(target_x), float(target_y), float(target_z + altitude_offset))
print('Flying to: ', point)
vehicle.simple_goto(point, groundspeed=5)
    
while True:
    with open('fly_to_point.csv', 'a') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=headers)

        info = {
            'lat':x,
            'long':y,
            'alt':z,
            'time':t
        }

        csv_writer.writerow(info)
        print(x, y, z, t)
        t += delay
        x = (vehicle.location.global_frame.lat - home[0])*1e4 #scaling to get "readable values"
        y = (vehicle.location.global_frame.lon - home[1])*1e4
        z = vehicle.location.global_frame.alt - home[2]

    if (abs(vehicle.location.global_frame.lat - target_x) < 0.00001 and abs(vehicle.location.global_frame.lon
                                                                                     - target_y) < 0.00001):
        break 
    time.sleep(delay)
