import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

#hi

def plotter(i):
    data = pd.read_csv('fly_to_point.csv')
    target_x = data['lat'][0]*1e4
    target_y = data['long'][0]*1e4
    target_z = data['alt'][0]
    x = data['lat'][1:]
    y = data['long'][1:]
    z = data['alt'][1:]
    t = data['time'][1:]
    plt.subplot(211)
    plt.cla()
    plt.title('Live Location Visualizer')
    plt.plot(target_x, target_y, marker = '.', markersize = '10', color = 'r', label = 'Target Location')
    plt.plot(x, y, label = 'Follower Path')
    plt.xlabel('Relative Latitude (1e-4 deg)')
    plt.ylabel('Relative Longitdue (1e-4 deg)')
    plt.xlim(-10, 10)
    plt.ylim(-10, 10)
    plt.legend(loc = 'upper left')
    plt.grid(True)

    plt.subplot(212)
    plt.cla()
    plt.plot(t, z, label = 'Follower Altitude')
    plt.axhline(y = target_z, color = 'r', label = 'Target Altitude', alpha = 0.6)
    plt.fill_between(t, y1 = target_z, y2 = 0, color = 'r', alpha = 0.2)
    plt.xlabel('Time (s)')
    plt.ylabel('Altitude (m)')
    plt.xlim(0, 15)
    plt.ylim(0, 50)
    plt.legend(loc = 'upper left')
    plt.grid(True)

animation = FuncAnimation(plt.gcf(), plotter, interval = 100)
plt.show()
