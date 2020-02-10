import platform
import subprocess
import sys
import distutils
import time

def is_windows():
    return platform.system() == 'Windows'


def check_path(path):
    try:
        ret = subprocess.check_output('rclone --config {} --disable ListR size \"{}\"'.format('rclone.conf', path),
                                      shell=True)
        print('It is okay:\n{}'.format(ret.decode('utf-8').replace('\0', '')))
    except subprocess.SubprocessError as error:
        sys.exit(str(error))


def print_during(time_start):
    time_stop = time.time()
    hours, rem = divmod((time_stop - time_start), 3600)
    minutes, sec = divmod(rem, 60)
    print("Elapsed Time: {:0>2}:{:0>2}:{:05.2f}".format(int(hours), int(minutes), sec))


def check_rclone_exists():
    rclone_prog = 'rclone'
    if is_windows():
        rclone_prog += ".exe"
    ret = distutils.spawn.find_executable(rclone_prog)
    if ret is None:
        sys.exit("To use AutoRclone you must install rclone first: https://rclone.org/downloads/")
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

# Calculate path size in bytes using rclone
def calculate_path_size(path, config_file):
    response = subprocess.check_output('rclone --config {} size \"{}\"'.format(config_file, path), shell=True, stderr=subprocess.DEVNULL)
    response_processed = response.decode('utf-8').replace('\0', '')
    response_bytes = response_processed.split('(')[1]
    response_bytes = response_bytes.replace('Bytes)', '').strip()

    return response_bytes
