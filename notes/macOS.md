# macOS

```sh
# system information
systemstats
system_profiler
sw_vers

# Terminal renaming
printf "\e]1;%s\a" {{ name }} # tabs
printf "\e]2;%s\a" {{ name }} # window

# set hostname
sudo scutil --set HostName "hostname.local"
sudo scutil --set LocalHostName "hostname"
sudo scutil --set ComputerName "hostname"
sudo dscacheutil -flushcache

# disable auto-boot on keypress
sudo nvram AutoBoot=%00

# get battery status
pmset -g batt | grep -E 'InternalBattery' | cut -f2 | awk -F\; '{print $1$2}'

# send to Safari reading list
osascript -e 'tell application "Safari" to add reading list item "<url>"'
```

---

```sh
# install macOS updates and reboot
sudo softwareupdate -aiR

# write a Brewfile
brew bundle dump

# uninstall all dependencies not listed in Brewfile
brew bundle cleanup --force

# get app version
brew info alacritty --cask --json=v2 | jq -r '.casks[].version'
brew info toilet --json=v2 | jq -r '.formulae[].versions.stable'
```

---

Fix a stuck screensaver:
`Ctrl+Cmd+Q` + `Esc`
