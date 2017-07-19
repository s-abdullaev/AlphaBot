# This version uses new-style automatic setup/destroy/mapping
# Need to change /etc/webiopi

# Imports
import webiopi
from webiopi.devices.serial import Serial

#ser = Serial("/dev/ttyAMA0",115200)
ser = Serial("/dev/ttyS0",115200)
# -------------------------------------------------- #
# Macro definition part                              #
# -------------------------------------------------- #
@webiopi.macro
def go_forward():
	ser.writeString("{\"Car\":\"Forward\"}")

@webiopi.macro
def go_backward():
	ser.writeString("{\"Car\":\"Backward\"}")

@webiopi.macro
def turn_left():
	ser.writeString("{\"Car\":\"Left\"}")

@webiopi.macro
def turn_right():
	ser.writeString("{\"Car\":\"Right\"}")

@webiopi.macro
def stop():
	ser.writeString("{\"Car\":\"Stop\"}")
    
@webiopi.macro
def set_speed(value):
	ser.writeString("{\"Car\":\"SetSpeed\",\"Value\":["+ value + ","+ value + "]}")	
	
@webiopi.macro
def set_servo1(value):
	ser.writeString("{\"Servo\":\"Servo1\",\"Angle\":"+ value + "}")	

@webiopi.macro
def set_servo2(value):
	ser.writeString("{\"Servo\":\"Servo2\",\"Angle\":"+ value + "}")	

# Called by WebIOPi at script loading
def setup():
	print("serial start...")
	ser.writeString("Hello World !!!")

# Called by WebIOPi at server shutdown
def destroy():
	if ser != None:
		ser.close()
    
