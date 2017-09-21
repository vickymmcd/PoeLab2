#!/usr/local/bin/python

from serial import Serial, SerialException

cxn = Serial('/dev/ttyACM1', baudrate=9600)

while(True):
    try:
        cmd_id = int(input("Please enter a command ID (1 - start the sweep, 0 - cancel sweep/stop: "))
        if int(cmd_id) > 1 or int(cmd_id) < 0:
            print ("Values other than 0 or 1 are ignored.")
        else:
            cxn.write([int(cmd_id)])
            while cxn.inWaiting() < 1:
                pass
            result = cxn.readline();
            print (result)
    except ValueError:
        print ("You must enter an integer value between 1 and 3.")
