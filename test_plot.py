import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

threshold = 5

def plotter(i):
    data = pd.read_csv('sampledata.csv')
    x = data['x_loc']
    y = data['y_loc']
    z = data['z_loc']
    t = data['time']
    plt.subplot(211)
    plt.cla()
    plt.plot(-12, -15, marker = '.', markersize = '10', color = 'r', label = 'Target Location')
    plt.plot(x, y, label = 'Follower Path')
    plt.xlabel('x Position')
    plt.ylabel('y Position')
    plt.xlim(-20, 20)
    plt.ylim(-20, 20)
    plt.legend(loc = 'best')
    plt.grid(True)

    plt.subplot(212)
    plt.cla()
    plt.plot(t, z, label = 'Follower Altitude')
    plt.axhline(y = threshold, color = 'r', label = 'Target Altitude', alpha = 0.6)
    plt.fill_between(t, y1 =threshold, y2 = 0, color = 'r', alpha = 0.2)
    plt.xlabel('Time')
    plt.ylabel('z Position')
    plt.xlim(0, 20)
    plt.ylim(0, 20)
    plt.legend(loc = 'best')
    plt.grid(True)

animation = FuncAnimation(plt.gcf(), plotter, interval = 1000)
plt.show()
