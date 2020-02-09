# AutoRclone Rewrite

NOTE: This is a work in progress, here is a todo list
## TODO:
- [ ] Add estimated time of completion
- [ ] Rewrite output, make it less ugly, proposed layout: `[AutoRclone Rewrite] (Job Name) amount transferred/total transfer amount @ <transfer speed here> SA: <num of SA here> ETA: <ETA Here>`
- [ ] Add command line arg to choose between copy or move
- [x] Add bandwidth Limiting 
- [ ] Implement proper support for encrypted sources and destinations
- [ ] Remove rc connect failed output messages to reduce confusion
- [x] Add more command line args to set rclone args
- [x] Make rclone command much less hardcoded
- [ ] Allow reading remotes from external rclone config

*Instructions will be written once the rewrite is complete.*

## Changelog

### 9th February 2020
- Removed old README content
- Removed `AutoRclone.jpg`
- Renamed `rclone_sa_magic.py` to `autorclone.py` 
- Added instructions note
- Implemented bandwidth limiting with `--bwlimit` arg
- Added many command line args to change rclone settings instead of them being hardcoded
- Fixed some readme formatting