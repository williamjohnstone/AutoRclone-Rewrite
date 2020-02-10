# AutoRclone Rewrite

Original Repository: https://github.com/xyou365/AutoRclone

NOTE: This is a work in progress, here is a todo list
## TODO:
- [ ] Add estimated time of completion
- [ ] Rewrite output, make it less ugly, proposed layout: `[AutoRclone Rewrite] (Job Name) amount transferred/total transfer amount @ <transfer speed here> SA: <num of SA here> ETA: <ETA Here>`
- [x] Add command line args to choose between copy, move or sync
- [x] Add bandwidth Limiting 
- [x] Implement proper support for encrypted sources and destinations
- [ ] Remove rc connect failed output messages to reduce confusion
- [x] Add more command line args to set rclone args
- [x] Make rclone command much less hardcoded
- [x] Allow reading remotes from external rclone config
- [ ] Add better logging
- [ ] Rewrite `add_to_google_group.py`, `add_to_team_drive.py` and `gen_sa_accounts.py` to make them more intuitive and fix broken english
- [ ] Write instructions

*Instructions will be written once the rewrite is complete.*

## Changelog

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
- Added many command line args to change rclone settings instead of them being hardcoded
- Fixed some readme formatting
- Added `.gitignore`
- Moved a lot of functions from main script to seperate files
- Added rclone config parser
- Added copy and move args
- Remove support for python 2
- Implement rclone config parser
- Remove todo from top of `autorclone.py`
- Moved source and destination parsing outside of massive loop to increase efficiency when generating config files
