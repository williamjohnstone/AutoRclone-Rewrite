# AutoRClone Rewrite

Original Repository: https://github.com/xyou365/AutoRclone

NOTE: This is a work in progress, here is a todo list

## TODO

- [ ] Add ability to watch folder
- [x] Add estimated time of completion
- [ ] Fix ETA for some edge cases (syncing files, etc. where whole source will not be transferred)
- [x] Rewrite output, make it less ugly, proposed layout: `[AutoRClone] (Job Name) amount transferred/total transfer amount @ <transfer speed here> SA: <num of SA here> ETA: <ETA Here>`
- [x] Add command line args to choose between copy, move or sync
- [x] Add bandwidth Limiting
- [x] Implement proper support for encrypted sources and destinations
- [x] Remove rc connect failed output messages to reduce confusion
- [x] Add more command line args to set RClone args
- [x] Make RClone command much less hardcoded
- [x] Allow reading remotes from external RClone config
- [x] Add better logging
- [ ] Rewrite `add_to_google_group.py`, `add_to_team_drive.py` and `gen_sa_accounts.py` to make them more intuitive and fix broken english
- [ ] Write instructions
- [ ] Add debug logging
- [x] Replace all prints with new logger
- [x] Replace `sys.exit()` calls with messages with proper logging
- [x] Implement my own transfer speed calculator as the speeds RClone is reporting seem to be off
- [x] Retain amount transferred between SAs
- [ ] Automatically rotate SAs that have reached their 24hr quota
- [x] Ignore no bytes transferred if file checks are increasing
- [ ] Finish command line argument documentation

*Instructions will be written once the rewrite is complete.*

## Documentation

PLEASE NOTE: This documentation is not complete.

### Reading Remotes from an RClone config file

One of the main benefits of this rewrite is being able to read your existing rclone remotes and use them to transfer data. To use this feature you must specifiy an rclone config file, for this, use the `--rclone-config-path` argument as shown below.

`python3 autorclone.py --copy `

`python3 autorclone.py --sync -s g-media-crypt -sp media/ -d g-media-crypt-2 -
dp media/ --rclone-config-path /root/.config/rclone/rclone.conf --drive-chunk-size 64M --transfers 8  --sa-start-id 9`

### Command Line Arguments

#### copy

Description: **Copy files from source to destination.**
Example Usage: `python3 autorclone.py --copy -s <source> -d <destination>`

#### move

Description: **Move files from source to destination.**
Example Usage: `python3 autorclone.py --move -s <source> -d <destination>`

#### sync

Description: **Sync the source to the destination, changing the destination only. Doesn’t transfer unchanged files.**
Example Usage: `python3 autorclone.py --sync -s <source> -d <destination>`

#### source

Shorthand: `s`
Description: **The source of your files. ID of Team Drive, ID of publicly shared folder or an RClone remote (Must use --rclone-config-path).**
Example Usage: `python3 autorclone.py --copy -s <source> -d <destination>`

#### destination

Shorthand: `d`
Description: **The destination for your files. ID of Team Drive, ID of publicly shared folder or an RClone remote (Must use --rclone-config-path).**
Example Usage: `python3 autorclone.py --copy -s <source> -d <destination>`

#### source-path

Shorthand: `sp`
Description: **The folder path inside source. (Local Path or path in Google Drive).**
Example Usage: `python3 autorclone.py --copy -s <source> -sp somefolder/subfolder -d <destination>`
Default: 

#### destination-path

Shorthand: `dp`
Description: **The folder path inside the destination. (Local path or path in Google Drive).**
Example Usage: `python3 autorclone.py --copy -s <source> -d <destination> -dp somefolder/subfolder`
Default: 

#### name

Shorthand: `n`
Description: **Copy files from source to destination.**
Example Usage: `python3 autorclone.py --copy -s <source> -d <destination>`

#### log-file

Description: **Copy files from source to destination.**
Example Usage: `python3 autorclone.py --copy -s <source> -d <destination>`

#### rclone-log-file

Description: **Copy files from source to destination.**
Example Usage: `python3 autorclone.py --copy -s <source> -d <destination>`

#### service-account-dir

Description: **Copy files from source to destination.**
Example Usage: `python3 autorclone.py --copy -s <source> -d <destination>`

#### port

Description: **Copy files from source to destination.**
Example Usage: `python3 autorclone.py --copy -s <source> -d <destination>`

#### sa-start-id

Description: **Copy files from source to destination.**
Example Usage: `python3 autorclone.py --copy -s <source> -d <destination>`

#### sa-end-id

Description: **Copy files from source to destination.**
Example Usage: `python3 autorclone.py --copy -s <source> -d <destination>`

#### rclone-config-path

Description: **Copy files from source to destination.**
Example Usage: `python3 autorclone.py --copy -s <source> -d <destination>`

#### dry-run

Description: **Copy files from source to destination.**
Example Usage: `python3 autorclone.py --copy -s <source> -d <destination>`

#### bwlimit

Description: **Copy files from source to destination.**
Example Usage: `python3 autorclone.py --copy -s <source> -d <destination>`

#### tpslimit

Description: **Copy files from source to destination.**
Example Usage: `python3 autorclone.py --copy -s <source> -d <destination>`

#### transfers

Description: **Copy files from source to destination.**
Example Usage: `python3 autorclone.py --copy -s <source> -d <destination>`

#### drive-chunk-size

Description: **Copy files from source to destination.**
Example Usage: `python3 autorclone.py --copy -s <source> -d <destination>`

#### delete-empty-src-dirs

Description: **Copy files from source to destination.**
Example Usage: `python3 autorclone.py --copy -s <source> -d <destination>`

#### create-empty-src-dirs

Description: **Copy files from source to destination.**
Example Usage: `python3 autorclone.py --copy -s <source> -d <destination>`

#### v

Description: **Copy files from source to destination.**
Example Usage: `python3 autorclone.py --copy -s <source> -d <destination>`

#### vv

Description: **Copy files from source to destination.**
Example Usage: `python3 autorclone.py --copy -s <source> -d <destination>`

#### debug

Description: **Copy files from source to destination.**
Example Usage: `python3 autorclone.py --copy -s <source> -d <destination>`

#### generated-config-path

Description: **Copy files from source to destination.**
Example Usage: `python3 autorclone.py --copy -s <source> -d <destination>`


