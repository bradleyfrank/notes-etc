# tmux

Move a process to tmux:

1. `ctrl-z`
2. `bg && disown %1`
3. Enter `tmux`
4. `reptyr $(pgrep myproc)`

Copying output:

* zero is the first line of the visible pane
* negative numbers are lines in the history
* the default is to capture only the visible contents of the pane

```
:capture-pane -S - # copy everything from beginning of history
:save-buffer /path/to/filename.txt
```

Move a tmux pane from one window to another:

```
:break-pane # <prefix> !
:join-pane -t <window-index> [-h|-v]
```

Setup a shared session:

```
tmux -S /tmp/shared new -s shared
sudo chgrp google-sudoers /tmp/shared
sudo chmod 775 /tmp/shared
# ...
tmux -S /tmp/shared attach -t shared
```