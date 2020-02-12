# AutoRClone Rewrite

Original Repository: https://github.com/xyou365/AutoRclone

NOTE: This is a work in progress, here is a todo list
## TODO:
- [x] Add estimated time of completion
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
- [ ] Use RClone rc to calculate transfer amount instead of size of source

*Instructions will be written once the rewrite is complete.*

## Changelog

### 12th February 2020
- Fixed divide by 0 bug in `helpers.calculate_transfer_eta()`
- Removed decimal place in eta
- Made sure source and destination paths are actually used
- Reverted `Changed output to 2 decimals in helpers.convert_bytes_to_best_unit()`
- Better transfer size checks (still not perfect as doesn't account for files that are already on the destination)
- Made sure arg parser uses utf8 encoding

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
