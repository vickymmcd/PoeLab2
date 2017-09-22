#!/usr/local/bin/python

from serial import Serial, SerialException

import json
import matplotlib.pyplot as plt

cxn = Serial('/dev/ttyACM0', baudrate=9600)
running = False
results_list = []
xs = []
ys = []

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
                with open('sweep_file') as f:
                    json.dump(results_list, f)
                for i, my_result in enumerate(results_list):
                    ys.append(my_result[2])
                    xs.append(my_result[0])
                plt.plot(xs, ys)

                plt.xlabel('Servo 1 Angle (degrees)')
                plt.ylabel('Distance (cm)')
                plt.title('Distance Graph')
                plt.grid(True)
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
            results_list.append((servo1angle, servo2angle, distance))
            print (str(result))
    except ValueError:
        print ("You must enter an integer value between 1 and 3.")
