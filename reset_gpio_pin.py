"""
This script will switch all GPIO Pin to LOW status
"""
from lib.utils import *
cfg = get_settings()

# Set all to 0
for slot in cfg['gpio_mapping']:
    # convert slot number into GPIO port number
    gpio_id = cfg['gpio_mapping'][int(slot)]
    execute_script(gpio_id, "LOW")
