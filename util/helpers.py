import platform
import subprocess
import sys
import distutils
import time
from pathlib import Path
import os

def is_windows():
    return platform.system() == 'Windows'


def calculate_duration(time_start):
    time_stop = time.time()
    hours, rem = divmod((time_stop - time_start), 3600)
    minutes, sec = divmod(rem, 60)
    return "{:0>2}:{:0>2}:{:05.2f}".format(int(hours), int(minutes), sec)


def check_rclone_exists():
    rclone_prog = 'rclone'
    if is_windows():
        rclone_prog += ".exe"
    #ret = distutils.spawn.find_executable(rclone_prog)
    ret = True
    if ret is None:
        sys.exit("To use AutoRClone you must install RClone first: https://rclone.org/downloads/")
    return ret


def convert_bytes_to_best_unit(bytes_value):
    bytes_value = float(bytes_value)

    value_tmp = bytes_value * 1e-15
    if value_tmp >= 1:
        return str(round(value_tmp, 1)) + "PB"

    value_tmp = bytes_value * 1e-12
    if value_tmp >= 1:
        return str(round(value_tmp, 1)) + "TB"

    value_tmp = bytes_value * 1e-9
    if value_tmp >= 1:
        return str(round(value_tmp, 1)) + "GB"

    value_tmp = bytes_value * 1e-6
    if value_tmp >= 1:
        return str(round(value_tmp, 1)) + "MB"

    value_tmp = bytes_value * 1e-3
    if value_tmp >= 1:
        return str(round(value_tmp, 1)) + "kB"

    return str(bytes_value) + "B"

# Calculate path size in bytes using RClone
def calculate_path_size(path, config_file):
    response = subprocess.check_output('rclone --config {} size \"{}\"'.format(config_file, path), shell=True, stderr=subprocess.DEVNULL)
    response_processed = response.decode('utf-8').replace('\0', '')
    response_bytes = response_processed.split('(')[1]
    response_bytes = response_bytes.replace('Bytes)', '').strip()

    return response_bytes


def log(msg, level, args, end=None):
    if level == "DEBUG" and not args.debug:
        return
    
    ts = time.gmtime()
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S", ts)
    message = '[{}] [AutoRClone] ({}) [{}] {}\n'.format(timestamp, args.name, level, msg)
    if end:
        print(message.replace('\n', ''), end=end)
    else:
        print(message.replace('\n', ''))
    # File logging
    file_path = args.log_file
    Path(os.path.split(file_path)[0]).mkdir(parents=True, exist_ok=True)
    logfile = open(file_path, 'a+')
    logfile.write(message)
    logfile.close()


def calculate_transfer_eta(bytes_to_transfer, transfer_speed_bytes):
    if bytes_to_transfer == 0 or transfer_speed_bytes == 0:
        return "Calculating ETA..."
    
    # time in seconds
    time = bytes_to_transfer / transfer_speed_bytes
    hours, rem = divmod((time), 3600)
    minutes, sec = divmod(rem, 60)
    eta_string = ""
    if hours > 1:
        eta_string += '{}h, '.format(int(hours))
    if minutes > 1:
        eta_string += '{}m, '.format(int(minutes))
    if sec > 1:
        eta_string += '{}s'.format(int(sec))

    return eta_string