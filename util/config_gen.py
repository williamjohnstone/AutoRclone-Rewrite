# I'm so sorry for the nest hell but I'm tired and don't know how to implement it better
import glob
import os
import sys
from util import config_parser

# For when a config file is specififed
def gen_remote_template(src_or_dest, parsed_config, args):
    remote_template = ""

    for remote in parsed_config:
        if remote.remote_name == args.source:
            if isinstance(remote, config_parser.crypt_remote):
                crypt_remote = remote.remote.split(':')[0]
                
                # Make this exit when found and also make it fall back on ids
                for dest_remote in parsed_config:
                    if dest_remote.remote_name == crypt_remote:
                        remote_template = '[{}{:03d}]\n' \
                            'type = drive\n' \
                            'scope = drive\n' \
                            'service_account_file = {}\n'
                        if remote.team_drive:
                            remote_template += '{} = {}\n\n'.format('team_drive', remote.team_drive)
                        elif remote.source_path_id:
                            remote_template += '{} = {}\n\n'.format('source_path_id', remote.source_path_id)
                    else:
                        print("Invalid rclone config, crypt remote with remote that does not exist!")
                        sys.exit(-1)

                remote_template += '[{}{:03d}_crypt]\n' \
                        'type = crypt\n' \
                        'remote = {}{:03d}:' + crypt_remote[1] + '\n' \
                        'filename_encryption = ' + remote.filename_encryption + '\n' \
                        'directory_name_encryption = ' + remote.directory_name_encryption + '\n' \
                        'password = ' + remote.password + '\n' 
                if remote.password2:
                    remote_template += 'password2 = ' + remote.password2 + '\n\n'
                else:
                    remote_template += '\n'
     
            else:
                remote_template = "[{}{:03d}]\n" \
                    "type = drive\n" \
                    "scope = drive\n" \
                    "service_account_file = {}\n"
                if remote.team_drive:
                    remote_template += "{} = {}\n".format("team_drive", remote.team_drive)
                elif remote.source_path_id:
                    remote_template += "{} = {}\n".format("source_path_id", remote.source_path_id)

    return remote_template


def gen_rclone_cfg(args):
    sa_files = glob.glob(os.path.join(args.service_account, '*.json'))
    output_of_config_file = './rclone_generated.conf'

    if len(sa_files) == 0:
        sys.exit('No json files found in ./{}'.format(args.service_account))

    source_remote = None
    dest_remote = None

    # If config file is listed attempt to read remote from parsed config
    if args.rclone_config_file:
        parsed_config = config_parser.parse_config(args.rclone_config_file)
        
        # Source parsing
        if args.source:
            source_remote = gen_remote_template(args.source, parsed_config, args)
        
        # Destination parsing
        dest_remote = gen_remote_template(args.destination, parsed_config, args)
                        

    with open(output_of_config_file, 'w') as fp:
        for i, filename in enumerate(sa_files):

            dir_path = os.path.dirname(os.path.realpath(__file__))
            filename = os.path.join(dir_path, filename)
            filename = filename.replace(os.sep, '/')

            

            # For source
            #if args.source_id:
            #    if len(args.source_id) == 33:
            #        folder_or_team_drive_src = 'root_folder_id'
            #    elif len(args.source_id) == 19:
            #        folder_or_team_drive_src = 'team_drive'
            #    else:
            #        sys.exit('Wrong length of team_drive_id or publicly shared root_folder_id')
            #
            #    text_to_write = "[{}{:03d}]\n" \
            #                    "type = drive\n" \
            #                    "scope = drive\n" \
            #                    "service_account_file = {}\n" \
            #                    "{} = {}\n".format('src', i + 1, filename, folder_or_team_drive_src, args.source_id)
            #
            #   
            #    # use path id instead path name
            #    if args.source_path_id:
            #        # for team drive only
            #        if len(args.source_id) == 19:
            #            if len(args.source_path_id) == 33:
            #                text_to_write += 'root_folder_id = {}\n'.format(args.source_path_id)
            #            else:
            #                sys.exit('Wrong length of source_path_id')
            #        else:
            #            sys.exit('For publicly shared folder please do not set -spi flag')
            #
            #    text_to_write += "\n"

            try:
                fp.write(source_remote)
            except:
                sys.exit("failed to write {} to {}".format(args.source_id, output_of_config_file))
            #else:
            #    pass

            # For destination
            #if len(args.destination_id) == 33:
            #    folder_or_team_drive_dst = 'root_folder_id'
            #elif len(args.destination_id) == 19:
            #    folder_or_team_drive_dst = 'team_drive'
            #else:
            #    sys.exit('Wrong length of team_drive_id or publicly shared root_folder_id')
            #
            #try:
            #    fp.write('[{}{:03d}]\n'
            #             'type = drive\n'
            #             'scope = drive\n'
            #             'service_account_file = {}\n'
            #             '{} = {}\n\n'.format('dst', i + 1, filename, folder_or_team_drive_dst, args.destination_id))
            #except:
            #    sys.exit("failed to write {} to {}".format(args.destination_id, output_of_config_file))

            # For crypt destination TODO: Rewrite
            #if args.crypt:
            #    remote_name = '{}{:03d}'.format('dst', i + 1)
            #    try:
            #        fp.write('[{}_crypt]\n'
            #                 'type = crypt\n'
            #                 'remote = {}:\n'
            #                 'filename_encryption = standard\n'
            #                 'password = hfSJiSRFrgyeQ_xNyx-rwOpsN2P2ZHZV\n'
            #                 'directory_name_encryption = true\n\n'.format(remote_name, remote_name))
            #    except:
            #        sys.exit("failed to write {} to {}".format(args.destination_id, output_of_config_file))

    return output_of_config_file, i