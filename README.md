# Smart Fridge NFC/RFID Sensor

## Installation

- python
- pip
- pip install tinkerforge
- pip install requests
- pip install datetime

## Configuration

Create a config.yml with the following content:

    tinkerforge:
      host: localhost
      port: 4223
      uid: uuV

    backend:
      url: https://aviatar-fridge.herokuapp.com/api/purchases
      salt: 1234567890
