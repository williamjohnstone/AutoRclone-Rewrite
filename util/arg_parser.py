import argparse

def parse_args():
    parser = argparse.ArgumentParser(description="Copy from source (local/publicly shared drive/Team Drive/) "
                                                 "to destination (publicly shared drive/Team Drive).")

    parser.add_argument('--copy', action='store_true',
                        help='Copy files from source to destination.')

    parser.add_argument('--move', action='store_true',
                        help='Move files from source to destination.')

    parser.add_argument('--sync', action='store_true',
                        help='Sync the source to the destination, changing the destination only. Doesn’t transfer unchanged files.')

    parser.add_argument('-s', '--source', type=str,
                        help='The source of your files. ID of Team Drive, ID of publicly shared folder or an rclone remote (Must use --rclone_config_file).')

    parser.add_argument('-d', '--destination', type=str, required=True,
                        help='The destination for your files. ID of Team Drive, ID of publicly shared folder or an rclone remote (Must use --rclone_config_file).')

    parser.add_argument('-sp', '--source_path', type=str, default='',
                        help='The folder path inside source. (Local Path or Path in Google Drive).')

    parser.add_argument('-dp', '--destination_path', type=str, default='',
                        help='The folder path of the destination. (in Google Drive).')

    parser.add_argument('-n', '--name', type=str, default="untitled",
                        help="Name your AutoRclone job, AutoRclone creates a log for each job, naming your jobs may be beneficial.")

    parser.add_argument('--log_dir', type=str, default="logs",
                        help="Relative path to logging directory.")

    parser.add_argument('--service_account_dir', type=str, default='accounts',
                        help='The directory path of json files for service account credentials.')

    parser.add_argument('--port', type=int, default=5572,
                        help='the port to run rclone rc. set it to different one if you want to run other instance.')

    parser.add_argument('--begin_sa_id', type=int, default=1,
                        help='Service account id to start with.')

    parser.add_argument('--end_sa_id', type=int, default=600,
                        help='Service account id to end with.')

    parser.add_argument('--rclone_config_file', type=str,
                        help='Path to existing config file with the source and destination remotes.')

    parser.add_argument('--dry_run', action='store_true',
                        help='For testing: make rclone dry-run.')

    parser.add_argument('--bwlimit', type=str, default='0',
                        help='Specify the desired bandwidth in kBytes/s, or use a suffix b|k|M|G. The default is 0 which means to not limit bandwidth. eg. 10M')

    parser.add_argument('--tpslimit', type=float, default=4,
                        help='Set the maximum amount of HTTP transactions per second. Use 0 used when no limit is required.')

    parser.add_argument('--transfers', type=int, default=4,
                        help='Sets the number of file transfers to be run in parallel.')

    parser.add_argument('--drive_chunk_size', type=str, default='8M',
                        help='Upload chunk size. Must a power of 2 >= 256k. Making this larger will improve performance, but note that each chunk is buffered in memory one per transfer.')

    parser.add_argument('--delete-empty-src-dirs', action='store_true',
                        help='Delete empty source dirs after move.')

    parser.add_argument('--create-empty-src-dirs', action='store_true',
                        help='Create empty source dirs on destination after sync.')

    parser.add_argument('-v', action='store_true',
                        help='Outputs information to log file about each transfer and prints stats once a minute by default.')

    parser.add_argument('-vv', action='store_true',
                        help='Outputs lots of debug info to the log file - useful for bug reports and really finding out what rclone is doing.')

    args = parser.parse_args()

    return args