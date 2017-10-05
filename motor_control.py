import RPi.GPIO as GPIO
import time

class CarControl(object):
    def __init__(self):
        GPIO.setmode(GPIO.BCM)

        self.fwdleft = 22 
        self.fwdright = 18

        self.revleft = 17 
        self.revright = 23

        self.motors = [self.fwdleft,self.fwdright,self.revleft,self.revright]

        for item in self.motors:
	    GPIO.setup(item, GPIO.OUT)

    def f(self,i):
	GPIO.output(self.fwdright, True)
	GPIO.output(self.fwdleft, True)
	time.sleep(i)
	GPIO.output(self.fwdright, False)
	GPIO.output(self.fwdleft, False)

    def l(self,i):
	GPIO.output(self.revright, True)
	GPIO.output(self.fwdleft, True)
	time.sleep(i)
	GPIO.output(self.revright, False)
	GPIO.output(self.fwdleft, False)	

    def r(self,i):
	GPIO.output(self.fwdright, True)
	GPIO.output(self.revleft, True)
	time.sleep(i)
	GPIO.output(self.fwdright, False)
	GPIO.output(self.revleft, False)

    def b(self,i):
	GPIO.output(self.revleft, True)
	GPIO.output(self.revright, True)
	time.sleep(i)
	GPIO.output(self.revleft, False)
	GPIO.output(self.revright, False)

