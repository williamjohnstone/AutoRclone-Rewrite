# AutoRclone Rewrite
#
# NOTE: This is a work in progress, here is a todo list
# TODO:
# - [ ] Add estimated time of completion
# - [ ] Rewrite output, make it less ugly, proposed layout: [AutoRclone Rewrite] (Job Name) amount transferred/total transfer amount @ <transfer speed here> SA: <num of SA here> ETA: <ETA Here>
# - [x] Add command line arg to choose between copy or move
# - [x] Add bandwidth Limiting 
# - [ ] Implement proper support for encrypted sources and destinations
# - [ ] Remove rc connect failed output messages to reduce confusion
# - [x] Add more command line args to set rclone args
# - [x] Make rclone command much less hardcoded
# - [ ] Allow reading remotes from external rclone config

import json
import io
import subprocess
import sys
import time
from signal import signal, SIGINT
from util import arg_parser, config_gen, config_parser, helpers

# =================modify here=================
logfile = "log_rclone.txt"  # log file: tail -f log_rclone.txt
PID = 0

# parameters for this script
SIZE_GB_MAX = 735  # if one account has already copied 735GB, switch to next account
CNT_DEAD_RETRY = 100  # if there is no files be copied for 100 times, switch to next account
CNT_SA_EXIT = 3  # if continually switch account for 3 times stop script

# change it when u know what are u doing
# paramters for rclone.
# If TPSLIMITxTRANSFERS is too big, will cause 404 user rate limit error,
# especially for tasks with a lot of small files
#TPSLIMIT = 3
#TRANSFERS = 3
# =================modify here=================

def handler(signal_received, frame):
    global PID

    if helpers.is_windows():
        kill_cmd = 'taskkill /PID {} /F'.format(PID)
    else:
        kill_cmd = "kill -9 {}".format(PID)

    try:
        print("\n" + " " * 20 + " {}".format(time.strftime("%H:%M:%S")))
        subprocess.check_call(kill_cmd, shell=True)
    except:
        pass
    sys.exit(0)

def main():
    signal(SIGINT, handler)

    # if rclone is not installed, exit
    ret = check_rclone_program()
    print("rclone is detected: {}".format(ret))
    args = arg_parser.parse_args()

    id = args.begin_sa_id
    end_id = args.end_sa_id

    config_file = args.rclone_config_file
    if config_file is None:
        print('generating rclone config file.')
        config_file, end_id = config_gen.gen_rclone_cfg(args)
        print('rclone config file generated.')
    else:
        return print('not supported yet.')
        pass
        # need parse labels from config files

    time_start = time.time()
    print("Start: {}".format(time.strftime("%H:%M:%S")))

    cnt_acc_error = 0
    while id <= end_id + 1:

        if id == end_id + 1:
            break
            # id = 1

        with io.open('current_sa.txt', 'w', encoding='utf-8') as fp:
            fp.write(str(id) + '\n')

        src_label = "src" + "{0:03d}".format(id) + ":"
        dst_label = "dst" + "{0:03d}".format(id) + ":"
        if args.crypt:
            dst_label = "dst" + "{0:03d}_crypt".format(id) + ":"

        if args.cache:
            dst_label = "dst" + "{0:03d}_cache".format(id) + ":"

        src_full_path = src_label + args.source_path
        if args.source_id is None:
            src_full_path = args.source_path

        dst_full_path = dst_label + args.destination_path
        if args.destination_id is None:
            dst_full_path = args.destination_path

        if args.test_only:
            print('\nsrc full path\n', src_full_path)
            print('\ndst full path\n', dst_full_path, '\n')

        if args.check_path and id == args.begin_sa_id:
            print("Please wait. Checking source path...")
            check_path(src_full_path)

            print("Please wait. Checking destination path...")
            check_path(dst_full_path)

        # =================cmd to run=================
        rclone_cmd = "rclone --config {} copy ".format(config_file)
        if args.dry_run:
            rclone_cmd += "--dry-run "
        rclone_cmd += "--drive-server-side-across-configs --rc --rc-addr=\"localhost:{}\" -vv ".format(args.port)
        rclone_cmd += "--tpslimit {} --transfers {} --drive-chunk-size {} ".format(args.tpslimit, args.transfers, args.drive_chunk_size)
        rclone_cmd += "--bwlimit {} ".format(args.bwlimit)
        rclone_cmd += "--drive-acknowledge-abuse --log-file={} \"{}\" \"{}\"".format(logfile, src_full_path,
                                                                                     dst_full_path)

        if not helpers.is_windows():
            rclone_cmd = rclone_cmd + " &"
        else:
            rclone_cmd = "start /b " + rclone_cmd
        # =================cmd to run=================

        print(rclone_cmd)

        try:
            subprocess.check_call(rclone_cmd, shell=True)
            print(">> Let us go {} {}".format(dst_label, time.strftime("%H:%M:%S")))
            time.sleep(10)
        except subprocess.SubprocessError as error:
            return print("error: " + str(error))

        cnt_error = 0
        cnt_dead_retry = 0
        size_bytes_done_before = 0
        cnt_acc_sucess = 0
        already_start = False

        try:
            response = subprocess.check_output('rclone rc --rc-addr="localhost:{}" core/pid'.format(args.port), shell=True)
            pid = json.loads(response.decode('utf-8').replace('\0', ''))['pid']
            if args.test_only: print('\npid is: {}\n'.format(pid))

            global PID
            PID = int(pid)

        except subprocess.SubprocessError as error:
            pass

        while True:
            rc_cmd = 'rclone rc --rc-addr="localhost:{}" core/stats'.format(format(args.port))
            try:
                response = subprocess.check_output(rc_cmd, shell=True)
                cnt_acc_sucess += 1
                cnt_error = 0
                # if there is a long time waiting, this will be easily satisfied, so check if it is started using
                # already_started flag
                if already_start and cnt_acc_sucess >= 9:
                    cnt_acc_error = 0
                    cnt_acc_sucess = 0
                    if args.test_only: print(
                        "total 9 times success. the cnt_acc_error is reset to {}\n".format(cnt_acc_error))

            except subprocess.SubprocessError as error:
                # continually ...
                cnt_error = cnt_error + 1
                cnt_acc_error = cnt_acc_error + 1
                if cnt_error >= 3:
                    cnt_acc_sucess = 0
                    if args.test_only: print(
                        "total 3 times failure. the cnt_acc_sucess is reset to {}\n".format(cnt_acc_sucess))

                    print('No rclone task detected (possibly done for this '
                          'account). ({}/3)'.format(int(cnt_acc_error / cnt_error)))
                    # Regard continually exit as *all done*.
                    if cnt_acc_error >= 9:
                        print('All done (3/3).')
                        print_during(time_start)
                        return
                    break
                continue

            response_processed = response.decode('utf-8').replace('\0', '')
            response_processed_json = json.loads(response_processed)
            size_bytes_done = int(response_processed_json['bytes'])
            checks_done = int(response_processed_json['checks'])
            size_GB_done = int(size_bytes_done * 9.31322e-10)
            speed_now = float(int(response_processed_json['speed']) * 9.31322e-10 * 1024)

            # try:
            #     print(json.loads(response.decode('utf-8')))
            # except:
            #     print("have some encoding problem to print info")
            if already_start:
                print("%s %dGB Done @ %fMB/s | checks: %d files" % (dst_label, size_GB_done, speed_now, checks_done), end="\r")
            else:
                print("%s reading source/destination | checks: %d files" % (dst_label, checks_done), end="\r")

            # continually no ...
            if size_bytes_done - size_bytes_done_before == 0:
                if already_start:
                    cnt_dead_retry += 1
                    if args.test_only:
                        print('\nsize_bytes_done', size_bytes_done)
                        print('size_bytes_done_before', size_bytes_done_before)
                        print("No. No size increase after job started.")
            else:
                cnt_dead_retry = 0
                if args.test_only: print("\nOk. I think the job has started")
                already_start = True

            size_bytes_done_before = size_bytes_done

            # Stop by error (403, etc) info
            if size_GB_done >= SIZE_GB_MAX or cnt_dead_retry >= CNT_DEAD_RETRY:

                if helpers.is_windows():
                    # kill_cmd = 'taskkill /IM "rclone.exe" /F'
                    kill_cmd = 'taskkill /PID {} /F'.format(PID)
                else:
                    kill_cmd = "kill -9 {}".format(PID)
                print("\n" + " " * 20 + " {}".format(time.strftime("%H:%M:%S")))
                try:
                    subprocess.check_call(kill_cmd, shell=True)
                    print('\n')
                except:
                    if args.test_only: print("\nFailed to kill.")
                    pass

                # =================Finish it=================
                if cnt_dead_retry >= CNT_DEAD_RETRY:
                    try:
                        cnt_exit += 1
                    except:
                        cnt_exit = 1
                    if args.test_only: print(
                        "1 more time for long time waiting. the cnt_exit is added to {}\n".format(cnt_exit))
                else:
                    # clear cnt if there is one time
                    cnt_exit = 0
                    if args.test_only: print("1 time sucess. the cnt_exit is reset to {}\n".format(cnt_exit))

                # Regard continually exit as *all done*.
                if cnt_exit >= CNT_SA_EXIT:
                    print_during(time_start)
                    # exit directly rather than switch to next account.
                    print('All Done.')
                    return
                # =================Finish it=================

                break

            time.sleep(2)
        id = id + 1

    print_during(time_start)


if __name__ == "__main__":
    main()