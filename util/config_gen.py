import glob
import os
import sys

def gen_rclone_cfg(args):
    sa_files = glob.glob(os.path.join(args.service_account, '*.json'))
    output_of_config_file = './rclone.conf'

    if len(sa_files) == 0:
        sys.exit('No json files found in ./{}'.format(args.service_account))

    with open(output_of_config_file, 'w') as fp:
        for i, filename in enumerate(sa_files):

            dir_path = os.path.dirname(os.path.realpath(__file__))
            filename = os.path.join(dir_path, filename)
            filename = filename.replace(os.sep, '/')

            # For source
            if args.source_id:
                if len(args.source_id) == 33:
                    folder_or_team_drive_src = 'root_folder_id'
                elif len(args.source_id) == 19:
                    folder_or_team_drive_src = 'team_drive'
                else:
                    sys.exit('Wrong length of team_drive_id or publicly shared root_folder_id')

                text_to_write = "[{}{:03d}]\n" \
                                "type = drive\n" \
                                "scope = drive\n" \
                                "service_account_file = {}\n" \
                                "{} = {}\n".format('src', i + 1, filename, folder_or_team_drive_src, args.source_id)

                # use path id instead path name
                if args.source_path_id:
                    # for team drive only
                    if len(args.source_id) == 19:
                        if len(args.source_path_id) == 33:
                            text_to_write += 'root_folder_id = {}\n'.format(args.source_path_id)
                        else:
                            sys.exit('Wrong length of source_path_id')
                    else:
                        sys.exit('For publicly shared folder please do not set -spi flag')

                text_to_write += "\n"

                try:
                    fp.write(text_to_write)
                except:
                    sys.exit("failed to write {} to {}".format(args.source_id, output_of_config_file))
            else:
                pass

            # For destination
            if len(args.destination_id) == 33:
                folder_or_team_drive_dst = 'root_folder_id'
            elif len(args.destination_id) == 19:
                folder_or_team_drive_dst = 'team_drive'
            else:
                sys.exit('Wrong length of team_drive_id or publicly shared root_folder_id')

            try:
                fp.write('[{}{:03d}]\n'
                         'type = drive\n'
                         'scope = drive\n'
                         'service_account_file = {}\n'
                         '{} = {}\n\n'.format('dst', i + 1, filename, folder_or_team_drive_dst, args.destination_id))
            except:
                sys.exit("failed to write {} to {}".format(args.destination_id, output_of_config_file))

            # For crypt destination TODO: Rewrite
            if args.crypt:
                remote_name = '{}{:03d}'.format('dst', i + 1)
                try:
                    fp.write('[{}_crypt]\n'
                             'type = crypt\n'
                             'remote = {}:\n'
                             'filename_encryption = standard\n'
                             'password = hfSJiSRFrgyeQ_xNyx-rwOpsN2P2ZHZV\n'
                             'directory_name_encryption = true\n\n'.format(remote_name, remote_name))
                except:
                    sys.exit("failed to write {} to {}".format(args.destination_id, output_of_config_file))

            # For cache destination
            if args.cache:
                remote_name = '{}{:03d}'.format('dst', i + 1)
                try:
                    fp.write('[{}_cache]\n'
                             'type = cache\n'
                             'remote = {}:\n'
                             'chunk_total_size = 1G\n\n'.format(remote_name, remote_name))
                except:
                    sys.exit("failed to write {} to {}".format(args.destination_id, output_of_config_file))

    return output_of_config_file, i