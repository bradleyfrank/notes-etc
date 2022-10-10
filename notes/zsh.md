# Zsh

```sh
# show zsh right prompt only on active prompt
setopt transient_rprompt
```

```sh
# PWD is 5 segments by default, any longer and truncate to 1st segment and last 3 segments
%(5~|%-1~/.../%3~|%~)
```