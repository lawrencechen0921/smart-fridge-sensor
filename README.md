# Smart Fridge NFC/RFID Sensor

For the sensor you need a Raspberry Pi with a TinkerForge NFC/RFID Reader. This
project contains a Python script that continuously scans for RFID cards and does
a request to the SmartFridge as soon a Card has been detected.

### Config
Replace the link to the API Link in the python script.

### Run
On your Pi run `py rfid-sensor.py`. This should be a automatically restarting
SystemCtl or Systemd service.


## Installation

- python
- pip
- pip install tinkerforge requests datetime yml

## Configuration

Configuration is done via `config.yml` file.

      tinkerforge:
            host: localhost
            port: 4223
            uid: uuV

      backend:
            url: https://aviabar.herokuapp.com/api/purchases
            salt: 1234567890
