#!/usr/bin/python3


"""
    This script allow for reading of a finger and comparison of this finger with thoses saved in the internal memory 
    of the module.

    When a finger is read, the script will trigger the external script 'on_match_success.sh' if a match is found,
    and 'on_match_failed.sh' if no match is found.

    The script on_match_success.sh will receive two parameters, the first beeing the matching score and the second
    the finger template position in module memory.

    When triggering external scripts, the program wait for the scripts to finish.
"""

import subprocess, sys
from time import sleep
from pyfingerprint.pyfingerprint import PyFingerprint
from pyfingerprint.pyfingerprint import FINGERPRINT_CHARBUFFER1

BASE_PATH = sys.path[0]
ON_MATCH_SUCCESS_SCRIPT = BASE_PATH + '/' + 'on_match_success.sh'
ON_MATCH_FAILED_SCRIPT =  BASE_PATH + '/' + 'on_match_failed.sh'

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

# Infinite loop so the script never end
while True :
    
    ## Tries to search the finger and calculate hash
    try:
        print('Waiting for finger...')

        ## Wait for finger to be read as an image
        while sensor.readImage() == False :
            pass

        ## Converts read image to template and stores it in charbuffer 1
        sensor.convertImage(FINGERPRINT_CHARBUFFER1)

        ## Searchs for a matching template in reader internal memory
        result = sensor.searchTemplate()

        template_position = result[0]
        accuracy_score = result[1]

        if template_position == -1 :
            print('No match found!')
            print('Trigger script : {}'.format(ON_MATCH_FAILED_SCRIPT))
            subprocess.call([ON_MATCH_FAILED_SCRIPT])

        else:
            print('Found template at position #{}'.format(template_position))
            print('The accuracy score is: {}'.format(accuracy_score))
            print('Trigger script : {}'.format(ON_MATCH_SUCCESS_SCRIPT))
            subprocess.call([ON_MATCH_SUCCESS_SCRIPT, str(accuracy_score), str(template_position)])

        # Wait for two second before reading another finger
        sleep(2)


    except Exception as e:
        print('Operation failed!')
        print('Exception message: '.format(e))
        exit(1)
