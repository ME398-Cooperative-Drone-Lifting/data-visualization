import csv
import random
import time

fieldnames = ['x_loc', 'y_loc', 'z_loc', 'time']

delay = 1

x = 0
y = 0
z = 0
t = 0

with open('sampledata.csv', 'w') as csv_file:
    csv_writer = csv.DictWriter(csv_file, fieldnames = fieldnames)
    csv_writer.writeheader()

while True:
    with open('sampledata.csv', 'a') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        info = {
            'x_loc':x,
            'y_loc':y,
            'z_loc':z,
            'time':t
        }

        csv_writer.writerow(info)
        print(x, y, z, t)
        t += delay
        x += random.uniform(-3, 2)
        y += random.uniform(-3, 2)
        z += random.uniform(0, 1)
    time.sleep(delay)


        
        
