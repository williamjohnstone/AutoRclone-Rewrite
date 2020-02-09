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
    # promote if user has not install rclone
    rclone_prog = 'rclone'
    if is_windows():
        rclone_prog += ".exe"
    ret = distutils.spawn.find_executable(rclone_prog)
    if ret is None:
        sys.exit("To use AutoRclone you must install rclone first: https://rclone.org/downloads/")
    return ret
