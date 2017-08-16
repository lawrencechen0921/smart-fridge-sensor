#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tinkerforge.ip_connection import IPConnection
from tinkerforge.bricklet_nfc_rfid import BrickletNFCRFID
import yaml
import requests
import time
import hmac
import hashlib
import base64
import datetime
import time
import os
import yaml

PATH = os.path.dirname(os.path.abspath(__file__))
SUCCESS_SCRIPT = PATH + "/success-beep.py"
FAIL_SCRIPT = PATH + "/error-beep.py"

with open(PATH + "/config.yml", 'r') as ymlfile:
    cfg = yaml.load(ymlfile)

HOST = str(cfg['tinkerforge']['host'])
PORT = cfg['tinkerforge']['port']
UID =  str(cfg['tinkerforge']['uid']) # UID of your NFC/RFID Bricklet

HTTP_BACKEND = cfg['backend']['url']
SALT = str(cfg['backend']['salt'])

print "-----------------"
print "NFC / RFID Sensor"
print "-----------------"
print "Sensor " + UID + '@' + HOST + ":" +str(PORT)
print "Backend " + HTTP_BACKEND
print "-----------------"


tag_type = 0
blocked = False

#
# Send scanned id to the backend
#
def send_id(id):
    try:
        os.system("python " + SUCCESS_SCRIPT + " 1")
        timestamp = str(datetime.datetime.now())
        # Calcualte signature
        digest = hmac.new(SALT, msg=id + timestamp, digestmod=hashlib.sha256).digest()
        signature = base64.b64encode(digest).decode()

        print("Sending ID: '" + id + "', Time: " + timestamp  + ", Signature: '" + signature + "'")
        blocked = True
        # Send id to backend
        response = requests.post(HTTP_BACKEND, data={'id': id, 'time': timestamp, 'signature': signature }, timeout=10.0)
        # React on errors
        response.raise_for_status()
        # Check status
        if response.status_code == requests.codes.ok:
            print("Success.")
        else:
            print("Unexpected status code received: ", response.status_code, response.reason)
        blocked = False

    except requests.exceptions.HTTPError as err:
        os.system("python " + FAIL_SCRIPT + " 1")
        blocked = False
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
        id = "".join(map(str, map(hex, ret.tid[:ret.tid_length])))
        print("Detected tag with ID [" + id + "]")
        if blocked:
            print("Blocking duplicate read.")
        else:
            send_id(id)

#
# Main
#
if __name__ == "__main__":

    os.system("python " + SUCCESS_SCRIPT + " 1")

    ipcon = IPConnection() # Create IP connection
    nr = BrickletNFCRFID(UID, ipcon) # Create device object

    ipcon.connect(HOST, PORT) # Connect to brickd
    # Don't use device before ipcon is connected

    # Register state changed callback to function cb_state_changed
    nr.register_callback(nr.CALLBACK_STATE_CHANGED, lambda x, y: cb_state_changed(x, y, nr))

    # Start scan loop
    nr.request_tag_id(nr.TAG_TYPE_MIFARE_CLASSIC)

    while True:
        time.sleep(1)

    ipcon.disconnect()
