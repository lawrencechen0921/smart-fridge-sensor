#!/usr/bin/env python

import RPi.GPIO as GPIO   #import the GPIO library
import time #import the time library

buzzer_pin = 22                   #set the buzzer pin variable to number 18
GPIO.setmode(GPIO.BCM)#Use the Broadcom method for naming the GPIO pins
GPIO.setup(buzzer_pin, GPIO.OUT)  #Set pin 22 as an output pin

def buzz(pitch, duration):   #create the function "buzz" and feed it the pitch and duration)
 period = 1.0 / pitch     #in physics, the period (sec/cyc) is the inverse of the frequency (cyc/sec)
 delay = period / 2     #calcuate the time for half of the wave
 cycles = int(duration * pitch)   #the number of waves to produce is the duration times the frequency

 for i in range(cycles):    #start a loop from 0 to the variable "cycles" calculated above
   GPIO.output(buzzer_pin, True)   #set pin 18 to high
   time.sleep(delay)    #wait with pin 18 high
   GPIO.output(buzzer_pin, False)    #set pin 18 to low
   time.sleep(delay)    #wait with pin 18 low

  #feed the pitch and duration to the function, "buzz"

buzz(125.0, 0.2)
time.sleep(0.1)
buzz(125.0, 0.2)
time.sleep(0.1)
buzz(125.0, 0.2)

GPIO.cleanup()
