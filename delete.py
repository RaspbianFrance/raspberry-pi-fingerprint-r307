#!/usr/bin/python3

import time
from pyfingerprint.pyfingerprint import PyFingerprint
from pyfingerprint.pyfingerprint import FINGERPRINT_CHARBUFFER1
from pyfingerprint.pyfingerprint import FINGERPRINT_CHARBUFFER2

"""
    This script allow for deleting a fingerprint from the internal memory.
"""

## Tries to initialize the sensor
try:
    sensor = PyFingerprint('/dev/serial0', 57600, 0xFFFFFFFF, 0x00000000)

    if ( sensor.verifyPassword() == False ):
        raise ValueError('The fingerprint sensor is protected by password!')

except Exception as e:
    print('The fingerprint sensor could not be initialized!')
    print('Exception message: {}'.format(e))
    exit(1)

## Gets info about how many fingerprint are currently stored
print('Currently stored fingers: {}/{}'.format(sensor.getTemplateCount(), sensor.getStorageCapacity()))

## Tries to enroll new finger
try:
    position = input('Please enter the template position you want to delete: ')
    position = int(position)

    if sensor.deleteTemplate(position) == True :
        print('Fingerprint deleted!')

except Exception as e:
    print('Operation failed!')
    print('Exception message: '.format(e))
    exit(1)
