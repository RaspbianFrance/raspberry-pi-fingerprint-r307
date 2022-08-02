#!/usr/bin/python3

import time
from pyfingerprint.pyfingerprint import PyFingerprint
from pyfingerprint.pyfingerprint import FINGERPRINT_CHARBUFFER1
from pyfingerprint.pyfingerprint import FINGERPRINT_CHARBUFFER2

"""
    This script allow for enrolling of new fingers in the module internal memory.
    The script ask for two finger pressure in order to ensure the quality of finger image.
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
    # We read finger a first time
    print('Waiting for finger...')

    ## Wait for finger to be read as an image
    while sensor.readImage() == False :
        pass

    ## Converts read image to template and stores it in charbuffer 1
    sensor.convertImage(FINGERPRINT_CHARBUFFER1)

    ## Checks if finger is already enrolled to prevent double enroll
    result = sensor.searchTemplate()
    template_position = result[0]

    if template_position >= 0 :
        print('This finger already exists at position #{}'.format(template_position))
        exit(0)

    print('Remove finger...')
    time.sleep(2)

    # We read finger a second time to ensure the reading is of good enough quality
    print('Waiting for same finger again...')

    ## Wait that finger is read again
    while sensor.readImage() == False :
        pass

    ## Converts read image to template and stores it in charbuffer 2
    sensor.convertImage(FINGERPRINT_CHARBUFFER2)

    # Check if the two fingers image match, indicating a good quality of thoses images
    if ( sensor.compareCharacteristics() == 0 ):
        raise Exception('Fingers do not match')

    ## Turn our image to a template and save it in reader internal memory
    sensor.createTemplate()
    positionNumber = sensor.storeTemplate()
    print('Finger enrolled successfully!')
    print('New template position #{}'.format(positionNumber))

except Exception as e:
    print('Operation failed!')
    print('Exception message: '.format(e))
    exit(1)
