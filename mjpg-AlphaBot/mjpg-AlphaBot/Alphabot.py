# This veENBion uses new-style automatic setup/destroy/mapping
# Need to change /etc/webiopi

# Imports
import webiopi
import RPi.GPIO as GPIO
import time
from threading import Timer


# -------------------------------------------------- #
# Constants definition                               #
# -------------------------------------------------- #

# Left motor GPIOs
IN1=12 # H-Bridge 1
IN2=13 # H-Bridge 2
ENA=6 # H-Bridge 1,2EN

# Right motor GPIOs
IN3=20 # H-Bridge 3
IN4=21 # H-Bridge 4
ENB=26 # H-Bridge 3,4EN


#Infrared Obstacle Sensors
DR = 16
DL = 19

# Servo GPIOs
S1=27
S2=22
    
# Setup GPIOs
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)
GPIO.setup(IN3, GPIO.OUT)
GPIO.setup(IN4, GPIO.OUT)
GPIO.setup(ENA, GPIO.OUT)
GPIO.setup(ENB, GPIO.OUT)
GPIO.setup(DR,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(DL,GPIO.IN,pull_up_down=GPIO.PUD_UP)

GPIO.setup(S1, GPIO.OUT)
GPIO.setup(S2, GPIO.OUT)

# set software PWM 
PENA  = GPIO.PWM(ENA,500)
PENB  = GPIO.PWM(ENB,500)

PENA.start(50)
PENB.start(50)

PS1 = GPIO.PWM(S1,100)
PS1.start(50)
PS2 = GPIO.PWM(S2,100)
PS2.start(16)



def interp(range1, range2):
	def m(x): 
		d=float(x-range1[0])/float(range1[1]-range1[0])
		return d*(range2[1]-range2[0])+range2[0]
	return m

# -------------------------------------------------- #
# Macro definition part                              #
# -------------------------------------------------- #
@webiopi.macro
def set_speed(speed):
	PENA.ChangeDutyCycle(float(speed))
	PENB.ChangeDutyCycle(float(speed))

@webiopi.macro
def set_servo1(angle):
	m=interp([120, 0], [30,120])
	ang=m(float(angle))
	print("obtained angle: %s  computed angle: %s" % (angle, ang))
	PS1.ChangeDutyCycle(ang / 10.0 + 2.5)

@webiopi.macro
def set_servo2(angle):
	m=interp([0,180],[90,180])
	ang=m(float(angle))
	print("obtained angle: %s  computed angle: %s" % (angle, ang))
	PS2.ChangeDutyCycle(ang / 10.0 + 2.5)

@webiopi.macro
def go_forward():
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)

@webiopi.macro
def go_backward():
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)

@webiopi.macro
def turn_left():
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)
	
@webiopi.macro
def turn_right():
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.LOW)

@webiopi.macro
def stop():
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.LOW)
    
# Called by WebIOPi at script loading
def setup():
    # Setup GPIOs
    GPIO.setup(IN1, GPIO.OUT)
    GPIO.setup(IN2, GPIO.OUT)
    GPIO.setup(IN3, GPIO.OUT)
    GPIO.setup(IN4, GPIO.OUT)
    GPIO.setup(ENA, GPIO.OUT)
    GPIO.setup(ENB, GPIO.OUT)
    GPIO.setup(DR, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(DL, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    set_servo1(90)
    set_servo2(90)
    check_signals()

def check_signals():
    DR_status = GPIO.input(DR)
    DL_status = GPIO.input(DL)
    print("left pin %s: %s \t right pin %s: %s" % (DL, DL_status, DR, DR_status))
    if ((DL_status==0) or (DR_status==0)):
       go_backward()
       time.sleep(0.5)
       turn_left()
       time.sleep(0.5)
       stop()
    Timer(1, check_signals, ()).start()


# Called by WebIOPi at server shutdown
def destroy():
    # Reset GPIO functions

    GPIO.setup(IN1, GPIO.IN)
    GPIO.setup(IN2, GPIO.IN)
    GPIO.setup(IN3, GPIO.IN)
    GPIO.setup(IN4, GPIO.IN)
    GPIO.setup(ENA, GPIO.IN)
    GPIO.setup(ENB, GPIO.IN)
    
