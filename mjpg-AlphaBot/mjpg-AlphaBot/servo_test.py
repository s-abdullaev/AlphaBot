import RPi.GPIO as GPIO
import time


s1, s2= 27, 22

GPIO.setmode(GPIO.BCM)
GPIO.setup(s1, GPIO.OUT)
GPIO.setup(s2, GPIO.OUT)

pwm1=GPIO.PWM(s1, 100)
pwm2=GPIO.PWM(s2, 100)

pwm1.start(50)
pwm2.start(16)

def update(angle, pwm):
	duty=float(angle)/10.0+2.5
	pwm.ChangeDutyCycle(duty)


update(90, pwm1)
update(90, pwm2)

for i in range(90,180):
	print "servo2 %s" % i
	update(i, pwm2)
	time.sleep(0.5)

update(90, pwm2)

for i in range(30,120):
	print "servo1 %s" % i
	update(i, pwm1)
	time.sleep(0.5)

update(90, pwm1)
