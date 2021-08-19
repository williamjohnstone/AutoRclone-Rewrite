# AutoRClone Rewrite

Original Repository: https://github.com/xyou365/AutoRclone

NOTE: This is a work in progress, here is a todo list

## TODO

- [ ] Add ability to watch folder
- [ ] Rewrite `add_to_google_group.py`, `add_to_team_drive.py` and `gen_sa_accounts.py` to make them more intuitive and fix broken english
- [ ] Write instructions
- [ ] Add debug logging
- [ ] Finish command line argument documentation

~~
- [x] Add estimated time of completion
- [x] Fix ETA for some edge cases (syncing files, etc. where whole source will not be transferred)
- [x] Rewrite output, make it less ugly, proposed layout: `[AutoRClone] (Job Name) amount transferred/total transfer amount @ <transfer speed here> SA: <num of SA here> ETA: <ETA Here>`
- [x] Add command line args to choose between copy, move or sync
- [x] Add bandwidth Limiting
- [x] Implement proper support for encrypted sources and destinations
- [x] Remove rc connect failed output messages to reduce confusion
- [x] Add more command line args to set RClone args
- [x] Make RClone command much less hardcoded
- [x] Allow reading remotes from external RClone config
- [x] Add better logging
- [x] Replace all prints with new logger
- [x] Replace `sys.exit()` calls with messages with proper logging
- [x] Implement my own transfer speed calculator as the speeds RClone is reporting seem to be off
- [x] Retain amount transferred between SAs
- [x] Automatically rotate SAs that have reached their 24hr quota
- [x] Ignore no bytes transferred if file checks are increasing
~~
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

## Changelog

### 21st November 2020

- Updated `.gitignore` to exclude python venv files
- Changed some messages in the main script
- Commented some stuff that is broken so I can fix it later lmao
- Also this actually works which is news to me I thought it was broken :)
- Renamed `Readme.md` to `README.md`
- Added all current command line arguments to the documentation
- Start documentation

### 12th February 2020

- Fixed divide by 0 bug in `helpers.calculate_transfer_eta()`
- Removed decimal place in eta
- Made sure source and destination paths are actually used
- Reverted `Changed output to 2 decimals in helpers.convert_bytes_to_best_unit()`
- Better transfer size checks (still not perfect as doesn't account for files that are already on the destination)
- Made sure arg parser uses utf8 encoding
- Stopped error after pid fails to retrieve (this could mean transfers are done)
- Added message to notify account switching when error count reaches 3
- Fixed typo `Caclulating -> Calculating`
- Changed rclone command logging to debug log
- Added number to 3 successive error message

### 11th February 2020

- Changed output to 2 decimals in `helpers.convert_bytes_to_best_unit()`
- Added `--debug` arg
- Added `log` helper function
- Added a few command line arguments
- Made it possible to copy from remotes to local storage
- Changed all `rclone` in strings and comments to `RClone`
- Re-implemented RClone command
- Done lots of changes to `autorclone.py` over like 3 hours and I honestly don't remember what they are

### 10th February 2020

- Added stuff to `.gitignore` to prevent credential leaks
- Finished new config generation
- Fixed config gen loop logic
- Add new TODO
- Edited command line args and made helper text more helpful
- Added original repository to readme
- Removed some cmd line args
- Added `--log-dir` arg
- Added `calculate_path_size` helper function
- Implemented amount to transfer output

### 9th February 2020

- Removed old README content
- Removed `AutoRclone.jpg`
- Renamed `rclone_sa_magic.py` to `autorclone.py` 
- Added instructions note
- Implemented bandwidth limiting with `--bwlimit` arg
- Added many command line args to change RClone settings instead of them being hardcoded
- Fixed some readme formatting
- Added `.gitignore`
- Moved a lot of functions from main script to seperate files
- Added RClone config parser
- Added copy and move args
- Remove support for python 2
- Implement RClone config parser
- Remove todo from top of `autorclone.py`
- Moved source and destination parsing outside of massive loop to increase efficiency when generating config files
