import subprocess
import yaml
import os


def execute_script(port, status):
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


def get_time_delay_for_slot_and_volume(slot_volume_dict):
    print slot_volume_dict
    cfg = get_settings()
    list_timeout = []
    for el in slot_volume_dict:
        timeout_1cl_for_slot = cfg['gpio_mapping'][int(el['slot_id'])]['time_for_1cl']
        list_timeout.append(int(el['volume'])*timeout_1cl_for_slot)
    return max(list_timeout)
