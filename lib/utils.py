import subprocess
import yaml
import os


def execute_script(port, status):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    print current_dir
    cmd = "sudo python lib/switch_gpio_port_status.py --port "+str(port)+" --status "+status
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    p.communicate()


def get_settings():
    # Load settings. Will be used to convert slot number into GPIO pin number
    cfg = None
    __location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))
    with open(os.path.join(__location__, "../settings.yml")) as ymlfile:
        cfg = yaml.load(ymlfile)
    return cfg
