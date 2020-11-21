import glob
import os
import sys
from util import config_parser
from pathlib import Path
from util.helpers import log

def gen_remote_template(src_or_dest, parsed_config, args, is_config_file_specified):
    remote_template = None
    found = False
    remote_is_crypt = False
    
    if is_config_file_specified: 
        for remote in parsed_config:
            if remote.remote_name == src_or_dest:
                found = True

                if isinstance(remote, config_parser.crypt_remote):
                    crypt_remote_parts = remote.remote.split(':')
                    unencrypted_remote_found = False
                    remote_is_crypt = True
                
                    for unencrypted_remote in parsed_config:
                        if unencrypted_remote.remote_name == crypt_remote_parts[0]:
                            unencrypted_remote_found = True
                            remote_template = '[{}{:03d}]\n' \
                                'type = drive\n' \
                                'scope = drive\n' \
                                'service_account_file = {}\n'
                            if unencrypted_remote.team_drive:
                                remote_template += '{} = {}\n\n'.format('team_drive', unencrypted_remote.team_drive)
                            #elif unencrypted_remote.source_path_id:
                            #    remote_template += '{} = {}\n\n'.format('source_path_id', unencrypted_remote.source_path_id)
                        if unencrypted_remote_found:
                            break
                    if not unencrypted_remote_found:
                        log('Invalid RClone config, crypt remote with remote that does not exist!', 'ERROR', args)
                        sys.exit(-1)

                    remote_template += '[{}{:03d}_crypt]\n' \
                        'type = crypt\n' \
                        'remote = {}{:03d}:' + crypt_remote_parts[1] + '\n' \
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
                        remote_template += "{} = {}\n\n".format("team_drive", remote.team_drive)
                    elif remote.source_path_id:
                        remote_template += "{} = {}\n\n".format("source_path_id", remote.source_path_id)

            # If remote is found exit loop
            if found:
                break

    if not found:
        if len(src_or_dest) == 33:
            folder_or_team_drive_src = 'root_folder_id'
        elif len(src_or_dest) == 19:
            folder_or_team_drive_src = 'team_drive'
        elif is_config_file_specified:
            log('The config file ' + args.rclone_config_path + ' was specified, ' + src_or_dest +
                    ' was not a valid remote found in the config file, and is not a valid Team Drive ID or publicly shared Root Folder ID', "ERROR", args)
            sys.exit(-1)
        else:
            log(src_or_dest + ' is not a valid Team Drive ID or publicly shared Root Folder ID', 'ERROR', args)
            sys.exit(-1)
        remote_template = "[{}{:03d}]\n" \
            "type = drive\n" \
            "scope = drive\n" \
            "service_account_file = {}\n"
        remote_template += "{} = {}\n\n".format(folder_or_team_drive_src, src_or_dest)

    return remote_template, remote_is_crypt


def gen_rclone_cfg(args, filepath):
    sa_files = glob.glob(os.path.join(args.service_account_dir, '*.json'))

    if len(sa_files) == 0:
        log('No json files found in ./{}'.format(args.service_account_dir), 'ERROR', args)
        sys.exit(-1)

    source_remote = None
    dest_remote = None
    src_is_crypt = False
    dst_is_crypt = False
    
    is_config_file_specified = False
    parsed_config = None
    if args.rclone_config_path:
        is_config_file_specified = True
        parsed_config = config_parser.parse_config(args.rclone_config_path)

    # Source parsing
    if args.source:
        source_remote, src_is_crypt = gen_remote_template(args.source, parsed_config, args, is_config_file_specified)
        
    # Destination parsing
    if args.destination:
        dest_remote, dst_is_crypt = gen_remote_template(args.destination, parsed_config, args,is_config_file_specified)

    with open(filepath, 'w') as fp:
        for i, filename in enumerate(sa_files):

            dir_path = os.path.dirname(Path(os.path.realpath(__file__)).parent)
            filename = os.path.join(dir_path, filename)
            filename = filename.replace(os.sep, '/')
            index = i + 1

            if source_remote:
                if src_is_crypt:
                    remote_type = 'src'
                    fp.write(source_remote.format(remote_type, index, filename, remote_type, index, remote_type, index))
                else:
                    fp.write(source_remote.format('src', index, filename))

            if dest_remote:        
                if dst_is_crypt:
                    remote_type = 'dst'
                    fp.write(dest_remote.format(remote_type, index, filename, remote_type, index, remote_type, index))
                else:
                    fp.write(dest_remote.format('dst', index, filename))
                
    return i, src_is_crypt, dst_is_crypt