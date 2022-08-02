#!/usr/bin/python3


"""
    This script allow for capturing and saving on computer the raw image of a fingerprint.
"""

import sys, os
from pyfingerprint.pyfingerprint import PyFingerprint


def help () :
    print("""
        Usage : {} ./output_file.bmp
    """.format(os.path.realpath(__file__)))

    exit(0)


if len(sys.argv) < 2 :
    help()

OUTPUT_IMG_PATH = sys.argv[1]

## Tries to initialize the sensor
try:
    sensor = PyFingerprint('/dev/serial0', 57600, 0xFFFFFFFF, 0x00000000)

    if sensor.verifyPassword() == False :
        raise ValueError('The fingerprint sensor is protected by password!')

except Exception as e:
    print('The fingerprint sensor could not be initialized!')
    print('Exception message: {}'.format(e))
    exit(1)

## Gets info about how many fingerprint are currently stored
print('Currently stored fingers: {}/{}'.format(sensor.getTemplateCount(), sensor.getStorageCapacity()))

## Tries to search the finger and calculate hash
try:
    print('Waiting for finger...')

    ## Wait for finger to be read as an image
    while sensor.readImage() == False :
        pass

    print('Downloading image (this may take a while)...')

    sensor.downloadImage(OUTPUT_IMG_PATH)

    print('The image have been saved to "{}".'.format(OUTPUT_IMG_PATH))


except Exception as e:
    print('Operation failed!')
    print('Exception message: '.format(e))
    exit(1)