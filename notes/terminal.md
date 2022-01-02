# Terminal

## Zsh

```sh
# PWD is 5 segments by default, any longer and truncate to 1st segment and last 3 segments
%(5~|%-1~/.../%3~|%~)
```

## Vim

To comment blocks:

1. from normal mode enter enter visual block mode (`ctrl+v`)
2. select lines
3. `shift+i`
4. insert the line comment, e.g. `#`
5. press `esc esc`

To uncomment blocks:

1. from normal mode enter enter visual block mode (`ctrl+v`)
2. select lines
  a. use the left/right arrow keys to select more text
  b. to select chunks of text use shift + ←/→ arrow key
3. press `d` or `x` to delete characters, repeatedly if necessary

---

## tmux

Move a process to tmux:

1. `ctrl-z`
2. `bg && disown %1`
3. Enter `tmux`
4. `reptyr $(pgrep myproc)`

Copying output:

* zero is the first line of the visible pane
* negative numbers are lines in the history
* the default is to capture only the visible contents of the pane

```none
:capture-pane -S - # copy everything from beginning of history
:save-buffer /path/to/filename.txt
```

Move a tmux pane from one window to another:

```none
:break-pane # <prefix> !
:join-pane -t <window-index> [-h|-v]
```

---

|Name|Hex|R|G|B|Code|Name|
|--- |--- |--- |--- |--- |--- |--- |
|Base03|`#002b36`|0|43|54|234|brblack|
|Base02|`#073642`|7|54|66|235|black|
|Base01|`#586e75`|88|110|117|240|brgreen|
|Base00|`#657b83`|101|123|131|241|bryellow|
|Base0|`#839496`|131|148|150|244|brblue|
|Base1|`#93a1a1`|147|161|161|245|brcyan|
|Base2|`#eee8d5`|238|232|213|254|white|
|Base3|`#fdf6e3`|253|246|227|230|brwhite|
|Yellow|`#b58900`|181|137|0|136|yellow|
|Orange|`#cb4b16`|203|75|22|166|brred|
|Red|`#dc322f`|220|50|47|160|red|
|Magenta|`#d33682`|211|54|130|125|magenta|
|Violet|`#6c71c4`|108|113|196|61|brmagenta|
|Blue|`#268bd2`|38|139|210|33|blue|
|Cyan|`#2aa198`|42|161|152|37|cyan|
|Green|`#859900`|133|153|0|64|green|
