#!/usr/bin/env python
# -*- coding: utf-8 -*-

HOST = "localhost"
PORT = 4223
UID = "uuV" # UID of your NFC/RFID Bricklet
HTTP_BACKEND = "https://aviatar-fridge.herokuapp.com/api/purchases"
SALT = "1234567890"

from tinkerforge.ip_connection import IPConnection
from tinkerforge.bricklet_nfc_rfid import BrickletNFCRFID
import requests
import time
import hmac
import hashlib
import base64

tag_type = 0

#
# Send scanned id to the backend
#
def send_id(id):
    print("Sending ID " + id)
    try:
        # Calcualte signature
        digest = hmac.new(SALT, msg=id, digestmod=hashlib.sha256).digest()
        signature = base64.b64encode(dig).decode()
        # Send id to backend
        response = requests.post(HTTP_BACKEND, data={'id': id, 'signature': signature })
        # React on errors
        response.raise_for_status()
        # Check status
        if response.status_code = requests.ok.created:
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
    ipcon = IPConnection() # Create IP connection
    nr = BrickletNFCRFID(UID, ipcon) # Create device object

    ipcon.connect(HOST, PORT) # Connect to brickd
    # Don't use device before ipcon is connected

    # Register state changed callback to function cb_state_changed
    nr.register_callback(nr.CALLBACK_STATE_CHANGED,
                         lambda x, y: cb_state_changed(x, y, nr))

    # Start scan loop
    nr.request_tag_id(nr.TAG_TYPE_MIFARE_CLASSIC)

    raw_input("Press key to exit\n") # Use input() in Python 3
    ipcon.disconnect()
