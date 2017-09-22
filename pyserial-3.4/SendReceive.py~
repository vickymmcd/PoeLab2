#!/usr/local/bin/python

from serial import Serial, SerialException

cxn = Serial('/dev/ttyACM0', baudrate=9600)

while(True):
    try:
        cmd_id = int(input("Please enter a command ID (1 - read distance sensor, 2 - move the servo, 3 - move the other servo: "))
        if int(cmd_id) > 3 or int(cmd_id) < 1:
            print ("Values other than 1 2 or 3 are ignored.")
        else:
            cxn.write([int(cmd_id)])
            while cxn.inWaiting() < 1:
                pass
            result = cxn.readline();
            print (result)
    except ValueError:
        print ("You must enter an integer value between 1 and 3.")
