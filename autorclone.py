import json
import io
import subprocess
import sys
import time
from signal import signal, SIGINT
from util import arg_parser, config_gen, helpers
import hashlib

PID = 0

# Parameters for script
MAX_TRANSFER_BYTES = (740 * 1e9) # If one account has already copied 740GB (740 * 1e9), switch to next account
TRANSFER_DEAD_THRESHOLD = 60  # If no bytes are transferred after 60 loops (120 seconds), exit
SA_EXIT_TRESHOLD = 3  # If SAs are switched 3 successive times with no transfers, exit

# Exit handler to that kills the RClone process if the script is terminated
def exit_handler(signal_received, frame):
    global PID

    if helpers.is_windows():
        # Windows kill command
        kill_cmd = 'taskkill /PID {} /F'.format(PID)
    else:
        # Every other normal exit command
        kill_cmd = 'kill -9 {}'.format(PID)

    try:
        # Run the command
        subprocess.check_call(kill_cmd, shell=True)
    except:
        # Ignore errors
        pass
    # Exit the script
    sys.exit(0)

# Main function, everything is executed from here
def main():
    # Sets the scripts SIGINT handler to our exit_handler
    signal(SIGINT, exit_handler)

    # Check if RClone is installed, if it isn't, exit
    ret = helpers.check_rclone_exists()

    # Parse args
    args = arg_parser.parse_args()

    # Log that rclone was detected
    helpers.log('RClone detected: {}'.format(ret), 'INFO', args)

    # Generate config
    rclone_generated_config_path = args.generated_config_path

    source_path = ''

    # Use either source remote or source path, if neither exist exit
    if args.source:
        source_path = args.source
    elif args.source_path:
        source_path = args.source_path
    else:
        helpers.log('A source is required, please use either --source or --source_path.', 'ERROR', args)
        sys.exit(-1)

    # If both a remote and a path exist combine them using RClone syntax
    if args.source and args.source_path:
        source_path += ":" + args.source_path

    # See comments above
    destination_path = ''
    if args.destination:
        destination_path = args.destination
    elif args.destination_path:
        destination_path = args.destination_path
    else:
        helpers.log('A destination is required, please use either --destination or --destination_path.', 'ERROR', args)
        sys.exit(-1)

    if args.destination and args.destination_path:
        destination_path += ":" + args.destination_path

    # Set id initially to the starting SA id
    id = args.sa_start_id
    end_id = args.sa_end_id

    helpers.log('Generating RClone config file...', 'INFO', args)
    # Generate RClone config file
    end_id, src_is_crypt, dst_is_crypt = config_gen.gen_rclone_cfg(args, rclone_generated_config_path)

    time_start = time.time()
    helpers.log('Starting job: {}, at {}'.format(args.name, time.strftime('%H:%M:%S')), 'INFO', args)
    helpers.log('Source: ' + source_path, 'INFO', args)
    helpers.log('Destination: ' + destination_path, 'INFO', args)
    helpers.log('AutoRClone Log: ' + args.log_file, 'INFO', args)
    helpers.log('RClone Log: ' + args.rclone_log_file, 'INFO', args)
    helpers.log('Calculating source size, please wait', 'INFO', args)

    # Initialise exit counter outside of loop so it keeps it's value
    exit_counter = 0
    error_counter = 0
    global_bytes_transferred = 0
    while id <= end_id + 1:

        if id == end_id + 1:
            break
        
        # Construct destination and source labels
        src_label = 'src' + '{0:03d}'.format(id) + ':'
        dst_label = 'dst' + '{0:03d}'.format(id) + ':'
        if src_is_crypt:
            src_label = 'src' + '{0:03d}_crypt'.format(id) + ':'
        if dst_is_crypt:
            dst_label = 'dst' + '{0:03d}_crypt'.format(id) + ':'
        
        # Fix for local paths that do not use a remote
        if args.source_path:
            if not args.source:
                src_label = args.source_path
            else:
                src_label += args.source_path
        if args.destination_path:
            if not args.destination:
                dst_label = args.destination_path
            else:
                dst_label += args.destination_path

        if id == args.sa_start_id:
            amount_to_transfer_bytes = helpers.calculate_path_size(src_label, rclone_generated_config_path)
            amount_to_transfer = helpers.convert_bytes_to_best_unit(amount_to_transfer_bytes)
            helpers.log('Source size: ' + amount_to_transfer + '\n', 'INFO', args)

        # Construct RClone command
        rclone_cmd = 'rclone --config {} '.format(rclone_generated_config_path)
        if args.copy:
            rclone_cmd += 'copy '
        elif args.move:
            rclone_cmd += 'move '
        elif args.sync:
            rclone_cmd += 'sync '
        else:
            helpers.log('Please specify an operation (--copy, --move or --sync)', 'ERROR', args)
            sys.exit()

        rclone_cmd += '--drive-server-side-across-configs --drive-acknowledge-abuse --ignore-existing --rc '
        rclone_cmd += '--rc-addr=\"localhost:{}\" --tpslimit {} --transfers {} --drive-chunk-size {} --bwlimit {} --log-file {} '.format(
            args.port, args.tpslimit, args.transfers, args.drive_chunk_size, args.bwlimit, args.rclone_log_file)
        if args.dry_run:
            rclone_cmd += '--dry-run '
        if args.v:
            rclone_cmd += '-v '
        if args.vv:
            rclone_cmd += '-vv '
        if args.delete_empty_src_dirs:
            rclone_cmd += '--delete-empty-src-dirs '
        if args.create_empty_src_dirs:
            rclone_cmd += '--create-empty-src-dirs '

        # Add source and destination
        rclone_cmd += '\"{}\" \"{}\"'.format(src_label, dst_label)

        # If we're not on windows append ' &' otherwise append 'start /b ' to the start of rclone_cmd
        if not helpers.is_windows():
            rclone_cmd = rclone_cmd + " &"
        else:
            rclone_cmd = "start /b " + rclone_cmd

        try:
            subprocess.check_call(rclone_cmd, shell=True)
            helpers.log('Executing RClone command: {}'.format(rclone_cmd), 'DEBUG', args)
            time.sleep(10)
        except subprocess.SubprocessError as error:
            helpers.log('Error executing RClone command: {}'.format(error), 'ERROR', args)
            sys.exit(-1)

        # Counter for errors encountered when attempting to get RClone rc stats (per sa)
        sa_error_counter = 0
        # Counter that's incremented when no bytes are transferred over a time period
        dead_transfer_counter = 0
        # Updated on each loop
        last_bytes_transferred = 0
        # Counter for amount of successful stat retrievals from RClone rc (per sa)
        sa_success_counter = 0

        job_started = False

        # Get RClone PID and store it
        try:
            response = subprocess.check_output('rclone rc --rc-addr="localhost:{}" core/pid'.format(args.port), shell=True, stderr=subprocess.DEVNULL)
            pid = json.loads(response.decode('utf-8').replace('\0', ''))['pid']

            global PID
            PID = int(pid)
        except subprocess.SubprocessError as error:
            pass

        # Loop infinitely until loop is broken out of
        while True:
            # RClone rc stats command
            rc_cmd = 'rclone rc --rc-addr="localhost:{}" core/stats'.format(args.port)
            try:
                # Run command and store response
                response = subprocess.check_output(rc_cmd, shell=True, stderr=subprocess.DEVNULL)
                # Increment success counter
                sa_success_counter += 1
                # Reset error counter
                sa_error_counter = 0

                if job_started and sa_success_counter >= 9:
                    sa_error_counter = 0
                    sa_success_counter = 0

            except subprocess.SubprocessError as error:
                sa_error_counter += 1
                error_counter = error_counter + 1
                if sa_error_counter >= 3:
                    sa_success_counter = 0
                    if error_counter >= 9:
                        finish_job(args, time_start)
                        sys.exit(0)
                    helpers.log('Encountered 3 successive errors when trying to contact rclone, switching accounts ({}/3)'.format(error_counter/sa_error_counter), 'INFO', args)
                    break
                continue

            response_processed = response.decode('utf-8').replace('\0', '')
            response_processed_json = json.loads(response_processed)
            bytes_transferred = int(response_processed_json['bytes'])
            checks_done = int(response_processed_json['checks'])
            transfer_speed_bytes = (bytes_transferred - last_bytes_transferred) / 4
            # I'm using The International Engineering Community (IEC) Standard, eg. 1 GB = 1000 MB, if you think otherwise, fight me!
            best_unit_transferred = helpers.convert_bytes_to_best_unit(bytes_transferred)
            transfer_speed = helpers.convert_bytes_to_best_unit(transfer_speed_bytes)
            
            #transfers = response_processed_json['transferring']
            #for file in transfers:
            #    name = file['name']
            #    name_hashed = hashlib.sha1(bytes(name, encoding='utf8')).hexdigest()
            #    size_bytes = file['size']
            #    helpers.log('File: {} ({}) is {} bytes'.format(name, name_hashed, size_bytes), 'DEBUG', args)
            #    if not name_hashed in file_names:
            #        file_names.append(name_hashed)
            #        file_sizes.append(size_bytes)

            #helpers.log("file_names = " + str(file_names), 'DEBUG', args)
            #helpers.log("file_sizes = " + str(file_sizes), 'DEBUG', args)

            #amount_to_transfer_bytes = sum(file_sizes)
            #amount_to_transfer = helpers.convert_bytes_to_best_unit(amount_to_transfer_bytes)
            bytes_left_to_transfer = int(amount_to_transfer_bytes) - bytes_transferred
            eta = helpers.calculate_transfer_eta(bytes_left_to_transfer, transfer_speed_bytes)

            helpers.log('{}/{} @ {}/s Files Checked: {} SA: {} ETA: {}'.format(best_unit_transferred, amount_to_transfer, transfer_speed, checks_done, id, eta) + (" " * 10), "INFO", args, end='\r')

            # continually no ...
            if bytes_transferred - last_bytes_transferred == 0:
                dead_transfer_counter += 1
                helpers.log('No bytes transferred, RClone may be dead ({}/{})'.format(dead_transfer_counter, TRANSFER_DEAD_THRESHOLD) + (" " * 10), 'DEBUG', args)
            else:
                dead_transfer_counter = 0
                job_started = True

            last_bytes_transferred = bytes_transferred

            # Stop by error (403, etc) info
            if bytes_transferred >= MAX_TRANSFER_BYTES or dead_transfer_counter >= TRANSFER_DEAD_THRESHOLD:
                if helpers.is_windows():
                    kill_cmd = 'taskkill /PID {} /F'.format(PID)
                else:
                    kill_cmd = "kill -9 {}".format(PID)
                try:
                    subprocess.check_call(kill_cmd, shell=True)
                    helpers.log('Transfer limit reached or RClone is not transferring any data, switching service accounts', 'INFO', args)
                    amount_to_transfer_bytes -= bytes_transferred
                    amount_to_transfer = helpers.convert_bytes_to_best_unit(amount_to_transfer_bytes)
                    global_bytes_transferred += bytes_transferred
                except:
                    pass

                if dead_transfer_counter >= TRANSFER_DEAD_THRESHOLD:
                    try:
                        exit_counter += 1
                    except:
                        exit_counter = 1
                else:
                    # clear cnt if there is one time
                    exit_counter = 0

                # Regard continually exit as *all done*.
                if exit_counter >= SA_EXIT_TRESHOLD:
                    # Exit directly rather than switch to next account.
                    finish_job(args, time_start)
                    sys.exit(0)

                break

            time.sleep(4)
        id = id + 1

# TODO implement
def finish_job(args, time_start):
    helpers.log('Job FINISHED (this message will be better soon)', 'INFO', args)


if __name__ == "__main__":
    main()