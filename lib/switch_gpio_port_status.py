import RPi.GPIO as gpio
import argparse

# create arguments
parser = argparse.ArgumentParser(description='GPIO control')
parser.add_argument("--port", help="Port number")
parser.add_argument("--status", help="HIGH | LOW")

# parse arguments from script parameters
args = parser.parse_args()

if args.port and args.status:
    gpio_port = int(args.port)
    # option means that we are referring to the pins name instead of pin number
    gpio.setmode(gpio.BCM)
    gpio.setwarnings(False)
    # define port is output
    gpio.setup(gpio_port, gpio.OUT)
    # switch gpio port to 1
    if args.status == "HIGH":
        gpio.output(gpio_port, gpio.HIGH)
    else:
        gpio.output(gpio_port, gpio.LOW)
else:
    print "Usage: switch_gpio_port_status.py --port <port_number> --status <HIGH|LOW>"
