import RPi.GPIO as GPIO
from threading import Timer

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

#Infrared Obstacle Sensors
DR = 16
DL = 19

GPIO.setup(DR, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(DL, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def check_signals():
    DR_status = GPIO.input(DR)
    DL_status = GPIO.input(DL)
    print("left pin %s: %s \t right pin %s: %s" % (DL, DL_status, DR, DR_status))
    Timer(1, check_signals, ()).start()

check_signals()