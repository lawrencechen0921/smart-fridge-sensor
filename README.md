# Smart Fridge NFC/RFID Sensor

For the sensor you need a Raspberry Pi with a TinkerForge NFC/RFID Reader. This
project contains a Python script that continuously scans for RFID cards and executes
a request to the backend as soon a card has been detected.

## Installation

- `apt-get install python`
- `apt-get install pip`
- `pip install tinkerforge requests datetime pyyml`

## Configuration
Create a `config.yml` with the following content:

    tinkerforge:
      host: localhost
      port: 4223
      uid: uuV

    backend:
      url: https://aviatar-fridge.herokuapp.com/api/purchases
      salt: 1234567890

## Run
On your Pi run `py rfid-sensor.py`.

## Install as service
1. adjust the path to the script in the unit path
2. copy the provided unit file `aviabar-sensor.service` into
   `/usr/lib/systemd/system` or create a symbolic link at this location pointing
   to the file.
