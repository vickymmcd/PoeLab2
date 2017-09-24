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
            if '50,110,' in str(result):
                running = False
                cxn.write([0])
                cmd_id = 0
                with open('sweep_file.csv', 'w') as f:
                    json.dump(results_list, f)
                for i, my_result in enumerate(results_list):
                    '''3d stuff'''
                    '''if my_result[0] == 25:
                        xval = 0
                    elif my_result[0] > 25:
                        xval = math.sin(math.radians(my_result[0]) -25)*my_result[2]
                    else:
                        xval = -math.sin(math.radians(my_result[0]))*my_result[2]
                    if my_result[1] == 60:
                        yval = 0
                    elif my_result[1] > 60:
                        yval = math.sin(math.radians(my_result[1]) -60)*my_result[2]
                    else:
                        yval = -math.sin(math.radians(my_result[1]) -10)*my_result[2]'''
                    #xval = my_result[2]*math.cos(math.radians(my_result[0]))*math.sin(math.radians(my_result[1]))
                    #yval = my_result[2]*math.sin(math.radians(my_result[0]))*math.sin(math.radians(my_result[1]))
                    #zval = my_result[2]*math.cos(math.radians(my_result[1]))

                    '''2d version'''
                    '''xval = my_result[0]
                    yval = my_result[2]'''
                    ys.append(0)
                    xs.append(my_result[0])
                    zs.append(my_result[2])
                    #xs.append(xval)
                    #ys.append(yval)
                    #zs.append(zval)

                fig = plt.figure()
                #ax = fig.add_subplot(111, projection='3d')

                #ax.scatter(xs, ys, zs, c='r', marker='o')
                plt.scatter(xs, ys, c=zs, vmin=0, vmax=60, s=200)
                plt.colorbar()

                #ax.set_xlabel('Servo 1 Angle (degrees)')
                #ax.set_ylabel('Distance (cm)')

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
