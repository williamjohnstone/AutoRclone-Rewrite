import argparse

def parse_args():
    parser = argparse.ArgumentParser(description="Copy from source (local/publicly shared drive/Team Drive/) "
                                                 "to destination (publicly shared drive/Team Drive).")

    parser.add_argument('-c', '--copy', action='store_true',
                        help='Copy files from source to destination')

    parser.add_argument('-m', '--move', action='store_true',
                        help='Move files from source to destination')

    parser.add_argument('--sync', action='store_true',
                        help='Sync the source to the destination, changing the destination only. Doesn’t transfer unchanged files')

    parser.add_argument('-s', '--source_id', type=str,
                        help='the id of source. Team Drive id or publicly shared folder id')

    parser.add_argument('-d', '--destination_id', type=str, required=True,
                        help='the id of destination. Team Drive id or publicly shared folder id')

    parser.add_argument('-sp', '--source_path', type=str, default='',
                        help='the folder path of source. In Google Drive or local.')

    parser.add_argument('-dp', '--destination_path', type=str, default='',
                        help='the folder path of destination. In Google Drive.')

    # if there are some special symbols in source path, please use this
    # path id (publicly shared folder or folder inside team drive)
    parser.add_argument('-spi', '--source_path_id', type=str, default='',
                        help='the folder path id (rather than name) of source. In Google Drive.')

    parser.add_argument('-sa', '--service_account', type=str, default='accounts',
                        help='the folder path of json files for service accounts.')

    parser.add_argument('-cp', '--check_path', action='store_true',
                        help='if check src/dst path or not.')

    parser.add_argument('-p', '--port', type=int, default=5572,
                        help='the port to run rclone rc. set it to different one if you want to run other instance.')

    parser.add_argument('-b', '--begin_sa_id', type=int, default=1,
                        help='the begin id of sa for source')

    parser.add_argument('-e', '--end_sa_id', type=int, default=600,
                        help='the end id of sa for destination')

    # TODO: re-implement
    #parser.add_argument('-c', '--rclone_config_file', type=str,
    #                    help='config file path of rclone')
    
    parser.add_argument('-test', '--test_only', action='store_true',
                        help='for test: make rclone print some more information.')

    parser.add_argument('-t', '--dry_run', action='store_true',
                        help='for test: make rclone dry-run.')

    # TODO: Reimplement
    #parser.add_argument('--crypt', action="store_true",
    #                    help='for test: crypt remote destination.')

    parser.add_argument('--bwlimit', type=str, default='0',
                        help='Specify the desired bandwidth in kBytes/s, or use a suffix b|k|M|G. The default is 0 which means to not limit bandwidth. eg. 10M')

    parser.add_argument('--tpslimit', type=float, default=4,
                        help='Set the maximum amount of HTTP transactions per second. Use 0 used when no limit is required.')

    parser.add_argument('--transfers', type=int, default=4,
                        help='Sets the number of file transfers to be run in parallel.')

    parser.add_argument('--drive_chunk_size', type=str, default='8M',
                        help='Upload chunk size. Must a power of 2 >= 256k. Making this larger will improve performance, but note that each chunk is buffered in memory one per transfer.')

    parser.add_argument('--delete-empty-src-dirs', action='store_true',
                        help='Delete empty source dirs after move')

    parser.add_argument('--create-empty-src-dirs', action='store_true',
                        help='Create empty source dirs on destination after sync')

    args = parser.parse_args()

    return args