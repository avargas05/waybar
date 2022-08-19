"""Module to get CPU and GPU temperatures."""

import argparse
import json
import subprocess


def parse_args():
    """Parse the args."""
    parser = argparse.ArgumentParser(
        prog='temp_request',
        description='Gets the temp requested of cpu or gpu.')

    parser.add_argument(
        'unit',
        help='CPU or GPU temperature')

    return parser.parse_args()


def get_temps():
    """Get the temperature of the GPU."""
    process = subprocess.Popen(
        'sensors -j',
        shell=True,
        stdout=subprocess.PIPE)
    process.wait()
    stdout, err = process.communicate()
    if process.returncode == 0:
        temps = json.loads(stdout.decode('utf-8'))
        return temps
    else:
        print('Error:', err)

    return ''


def main():
    """Run argparse, get requested temp."""
    arg = parse_args()
    temps = get_temps()

    if arg.unit == 'cpu':
        temp = temps['k10temp-pci-00c3']['Tctl']['temp1_input']
        temp = round(temp)
        unit = ''
    elif arg.unit == 'gpu':
        temp = temps['amdgpu-pci-0e00']['junction']['temp2_input']
        temp = round(temp)
        unit = 'GPU'
    else:
        temp = 'NIL'

    # Round to the nearest ten to max of 80 for icon selection.
    if temp <= 44:
        temp_range = 40
    elif temp <= 54:
        temp_range = 50
    elif temp <= 64:
        temp_range = 60
    elif temp <= 74:
        temp_range = 70
    else:
        temp_range = 80

    temp_icon = {
        40: "",
        50: "",
        60: "",
        70: "",
        80: ""
    }

    icon = temp_icon[temp_range]
    degree = u'\N{DEGREE SIGN}' + 'C'

    command = f'echo {unit}{icon} {temp}{degree}'
    subprocess.run(command, shell=True)


if __name__ == '__main__':
    """Run main."""
    main()
