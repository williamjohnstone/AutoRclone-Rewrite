import platform
import subprocess
import sys
import re
import time
import pickledb
import math
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


# Inspired from https://stackoverflow.com/a/14822210
def convert_bytes_to_best_unit(bytes):
   if bytes == 0:
       return "0 Bytes"
   sizes = ("Bytes", "kB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
   i = int(math.floor(math.log(bytes, 1024)))
   s = round(bytes / math.pow(1024, i), 2)
   return str(s) + sizes[i]


# Calculate path size in bytes using RClone
def calculate_path_size(config_file, src_label, dst_label):
    cmd = ['rclone', '--config', config_file, 'copy', '--dry-run', src_label, dst_label]
    pattern = re.compile("([\d,]+\.\d+? [A-z]{6}), ([0-9]{1,3})", re.M)
    process = subprocess.Popen(cmd, shell=False, stderr=subprocess.PIPE)
    for line in process.stderr:
        match = re.search(pattern, line.decode('utf-8'))
        if match and match[2] == "100":
            return(rclone_size_to_bytes(match[1]))

# Inspired from https://stackoverflow.com/a/42865957
def rclone_size_to_bytes(size):
    units = {"B": 1, "KiByte": 10**3, "MiByte": 10**6, "GiByte": 10**9, "TiByte": 10**12}
    number, unit = [string.strip() for string in size.split()]
    return int(float(number)*units[unit])


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

def checkTimestamp(dst, save = False):
    dst = str(dst)
    db = pickledb.load('accounts.db', False)
    tmp_time = round(time.time())

    if save:
        db.set(dst, tmp_time)
        print('Account over limit. Saving into DB...')
        db.dump()
        return True

    # Time since limit is over 24h
    if db.get(dst) and tmp_time - db.get(dst) >= 86400:
        print('Over 24h since last limit! Using Account again...')
        return True
    # Time since limit is over 24h
    elif db.get(dst) and tmp_time - db.get(dst) < 86400:
        print('Under 24h since last limit! Not using Account again...')
        return False
    else:
        return True
    