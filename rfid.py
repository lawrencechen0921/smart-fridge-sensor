#!/usr/bin/env python
# -*- coding: utf-8 -*-

HOST = "localhost"
PORT = 4223
# UID = "uvB" # PLayground
UID = "uuV" # UID of your NFC/RFID Bricklet
HTTP_BACKEND = "https://aviatar-fridge.herokuapp.com/api/purchases"
SALT = "1234567890"
PIN1 = 7
PIN2 = 15

# Frequencies
c = 261
d = 294
e = 329
f = 349
g = 392
a = 440
b = 493
C = 423
r = 1

from tinkerforge.ip_connection import IPConnection
from tinkerforge.bricklet_nfc_rfid import BrickletNFCRFID
import requests
import time
import hmac
import hashlib
import base64
import time
import datetime
# import RPi.GPIO as GPIO

tag_type = 0

# pwm = GPIO.PWM(PIN2, 100)

#
# Beeps using Rapberry PI Piezo Beeper
#
def beep(numTimes, speed):
    GPIO.output(PIN1, True)
    GPIO.output(PIN2, True)
    time.sleep(speed) ## Wait
    p.start(100)             # start the PWM on 100  percent duty cycle
    p.ChangeDutyCycle(90)   # change the duty cycle to 90%
    p.ChangeFrequency(c)  # change the frequency to 261 Hz (floats also work)
    time.sleep(speed) ## Wait
    p.ChangeFrequency(d)  # change the frequency to 294 Hz (floats also work)
    time.sleep(speed) ## Wait
    p.ChangeFrequency(e)
    time.sleep(speed) ## Wait
    p.ChangeFrequency(f)
    time.sleep(speed) ## Wait
    p.ChangeFrequency(g)
    time.sleep(speed) ## Wait
    p.ChangeFrequency(a)
    time.sleep(speed) ## Wait
    p.ChangeFrequency(b)
    time.sleep(speed) ## Wait
    p.ChangeFrequency(C)
    time.sleep(speed) ## Wait
    p.ChangeFrequency(r)
    time.sleep(speed) ## Wait
    p.stop()         # stop the PWM output
    GPIO.cleanup()

#
# Send scanned id to the backend
#
def send_id(id):
    try:
        timestamp = str(datetime.datetime.now())
        # Calcualte signature
        digest = hmac.new(SALT, msg=id + timestamp, digestmod=hashlib.sha256).digest()
        signature = base64.b64encode(digest).decode()

        print("Sending ID: '" + id + "', Time: " + timestamp  + ", Signature: '" + signature + "'")
        # Send id to backend
        response = requests.post(HTTP_BACKEND, data={'id': id, 'time': timestamp, 'signature': signature })
        # React on errors
        response.raise_for_status()
        # Check status
        if response.status_code == requests.codes.created:
            print("Success.")
            time.sleep(2)
        else:
            print("Unexpected status code received: ", response.status_code, response.reason)
    except requests.exceptions.HTTPError as err:
        print ("Error occured.")
        print err

#
# Callback function for state changed callback
#
def cb_state_changed(state, idle, nr):
    # Cycle through all types
    if idle:
        global tag_type
        tag_type = (tag_type + 1) % 3
        nr.request_tag_id(tag_type)

    if state == nr.STATE_REQUEST_TAG_ID_READY:
        ret = nr.get_tag_id()
        print("Detected tag of type " + str(ret.tag_type) + " with ID [" + " ".join(map(str, map(hex, ret.tid[:ret.tid_length]))) + "]")
        send_id("".join(map(str, map(hex, ret.tid[:ret.tid_length]))))

if __name__ == "__main__":

#    GPIO.setmode(GPIO.BOARD)
#    GPIO.setup(PIN1, GPIO.OUT)
#    GPIO.setup(PIN2, GPIO.OUT)

    ipcon = IPConnection() # Create IP connection
    nr = BrickletNFCRFID(UID, ipcon) # Create device object

    ipcon.connect(HOST, PORT) # Connect to brickd
    # Don't use device before ipcon is connected

    # Register state changed callback to function cb_state_changed
    nr.register_callback(nr.CALLBACK_STATE_CHANGED, lambda x, y: cb_state_changed(x, y, nr))

    # Start scan loop
    nr.request_tag_id(nr.TAG_TYPE_MIFARE_CLASSIC)

    raw_input("Press key to exit\n") # Use input() in Python 3
    ipcon.disconnect()
