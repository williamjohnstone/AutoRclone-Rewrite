import sys
from dataclasses import dataclass

@dataclass
class drive_remote:
    remote_name: str
    team_drive: str
    root_folder_id: str


@dataclass
class crypt_remote:
    remote_name: str
    remote: str
    filename_encryption: str
    directory_name_encryption: bool
    # Hashed password and salt
    password: str
    password2: str


def parse_config(file_path):
    try:
        file = open(file_path, 'r')
    except FileNotFoundError:
        print("Rclone config file not found!")
        sys.exit(-1)

    config_content = file.read()
    remotes_unparsed = []

    remotes_tmp = config_content.split('[')
    
    for i in range(1, len(remotes_tmp)):
        remote_tmp = remotes_tmp[i].split(']\n')
        # ['Remote Name', 'Remote Data']
        remotes_unparsed.append([remote_tmp[0], remote_tmp[1]])

    remotes_parsed = []

    for remote in remotes_unparsed:
        name = remote[0]
        data = remote[1]
        properties = []

        data_tmp = data.split('\n')
        # Remove empty array items caused by \n characters
        data_tmp = list(filter(None, data_tmp))

        for data in data_tmp:
            data_split = data.split('=')
            # ['Property', 'Value']
            properties.append([data_split[0].strip(), data_split[1].strip()])

        remotes_parsed.append([name, properties])

    remotes = []

    for remote in remotes_parsed:
        name = remote[0]
        properties = remote[1]
        remote_type = None
        team_drive = None
        root_folder_id = None
        remote = None
        filename_encryption = None
        directory_name_encryption = None
        password = None
        password2 = None


        for prop in properties:

            if prop[0] == "type":
                remote_type = prop[1]
            elif prop[0] == "team_drive":
                team_drive = prop[1]
            elif prop[0] == "root_folder_id":
                root_folder_id = prop[1]
            elif prop[0] == "remote":
                remote = prop[1]
            elif prop[0] == "filename_encryption":
                filename_encryption = prop[1]
            elif prop[0] == "directory_name_encryption":
                directory_name_encryption = prop[1]
            elif prop[0] == "password":
                password = prop[1]
            elif prop[0] == "password2":
                password2 = prop[1]

        if remote_type == "drive":
            if team_drive or root_folder_id:
                new_remote = drive_remote(name, team_drive, root_folder_id)
            else:
                pass
        elif remote_type == "crypt":
            new_remote = crypt_remote(name, remote, filename_encryption, directory_name_encryption, password, password2)

        remotes.append(new_remote)
    return remotes