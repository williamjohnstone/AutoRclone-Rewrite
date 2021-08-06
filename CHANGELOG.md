# Changelog

## 6th August 2021

- Fixed dead transfer trigger during rclone file checks
- Fixed UnboundLocalError in config parser when remote is of type drive and has no root folder and isnt a team drive
- Moved Changelog to seperate file
- Fix gen_sa_accounts.py not filtering dead projects
- Add support for folder IDs with 28 characters
- Fixed incorrect naming in config parser `source_path_id` changed to `root_folder_id`

## 21st November 2020

- Updated `.gitignore` to exclude python venv files
- Changed some messages in the main script
- Commented some stuff that is broken so I can fix it later lmao
- Also this actually works which is news to me I thought it was broken :)
- Renamed `Readme.md` to `README.md`
- Added all current command line arguments to the documentation
- Start documentation

## 12th February 2020

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

## 11th February 2020

- Changed output to 2 decimals in `helpers.convert_bytes_to_best_unit()`
- Added `--debug` arg
- Added `log` helper function
- Added a few command line arguments
- Made it possible to copy from remotes to local storage
- Changed all `rclone` in strings and comments to `RClone`
- Re-implemented RClone command
- Done lots of changes to `autorclone.py` over like 3 hours and I honestly don't remember what they are

## 10th February 2020

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

## 9th February 2020

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
