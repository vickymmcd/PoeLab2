#!/usr/local/bin/python

from serial import Serial, SerialException

import json
import math
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


cxn = Serial('/dev/ttyACM0', baudrate=9600)
running = False
results_list = []
xs = []
ys = []
zs = []

while(True):
    try:
        if not running:
            cmd_id = int(input("Please enter a command ID (1 - start the sweep, 0 - cancel sweep/stop: "))
        if int(cmd_id) > 1 or int(cmd_id) < 0:
            print ("Values other than 0 or 1 are ignored.")
        else:
            cxn.write([int(cmd_id)])
            if cmd_id == 1:
                running = True
            while cxn.inWaiting() < 1:
                pass
            result = cxn.readline();
            if '110,110,' in str(result):
                running = False
                cxn.write([0])
                cmd_id = 0
                with open('sweep_file.csv', 'w') as f:
                    json.dump(results_list, f)
                for i, my_result in enumerate(results_list):
                    if my_result[2] <= 50:
                        '''3d stuff'''
                        '''xval = my_result[2]*math.cos(math.radians(my_result[0]))*math.sin(math.radians(my_result[1]))
                        yval = my_result[2]*math.sin(math.radians(my_result[0]))*math.sin(math.radians(my_result[1]))
                        zval = my_result[2]*math.cos(math.radians(my_result[1]))'''

                        '''2d version'''
                        xval = my_result[0]
                        yval = my_result[2]

                        xs.append(xval)
                        ys.append(yval)
                        #zs.append(zval)

                fig = plt.figure()
                '''ax = fig.add_subplot(111, projection='3d')

                #plt.scatter(xs, ys, c=zs, vmin=0, vmax=60, s=200)
                ax.scatter(xs, ys, zs)'''
                #plt.colorbar()

                plt.scatter(xs, ys)
                plt.xlabel('Servo 1 Angle (degrees)')
                plt.ylabel('Distance (cm)')

                plt.title('Distance Graph')
                plt.savefig("graph.png")
                plt.show()
            result = str(result)
            result = result.strip("\\r\\n'")
            result = result[2:]
            servo1angle = result[:result.index(',')]
            result = result[result.index(',')+1:]
            servo2angle = result[:result.index(',')]
            result = result[result.index(',')+1:]
            distance = result
            results_list.append((int(servo1angle), int(servo2angle), int(distance)))
            print (str(result))
    except ValueError:
        print ("You must enter an integer value between 1 and 3.")
