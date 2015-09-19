"""
Test all pump over the GPIO control lib.
Switch HIGH during 1 second and then back to LOW
"""
import time
from lib.utils import *


cfg = get_settings()

# First set all to 0
for slot in cfg['gpio_mapping']:
    # convert slot number into GPIO port number
    gpio_id = cfg['gpio_mapping'][int(slot)]
    execute_script(gpio_id, "LOW")

# Set all to 1 durring 1 second
for slot in cfg['gpio_mapping']:
    # convert slot number into GPIO port number
    gpio_id = cfg['gpio_mapping'][int(slot)]
    print "GPIO "+str(gpio_id)+" HIGH"
    execute_script(gpio_id, "HIGH")
    time.sleep(1)
    print "GPIO "+str(gpio_id)+" LOW"
    execute_script(gpio_id, "LOW")
