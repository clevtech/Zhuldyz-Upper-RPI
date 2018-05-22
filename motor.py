import RPi.GPIO as GPIO
from time import sleep
import socket

#pwm.stop()
GPIO.cleanup()

GPIO.setmode(GPIO.BOARD)
GPIO.setup(3, GPIO.OUT)
pwm=GPIO.PWM(3, 50)
pwm.start(0)

def SetAngle(angle):
        duty = int(angle) / 18 + 2
        GPIO.output(3, True)
        pwm.ChangeDutyCycle(duty)

        sleep(1)
        GPIO.output(3, False)
        GPIO.output(3, True)
        pwm.ChangeDutyCycle(0)
        sleep(1)
        GPIO.output(3, False)

