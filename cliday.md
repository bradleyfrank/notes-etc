# `#cliday`

`#cliday 2022-03-18`

1a. [zsh-syntax-highlighting](https://github.com/zsh-users/zsh-syntax-highlighting): syntax highlighting for Zsh
1b. [zsh-autosuggestions](https://github.com/zsh-users/zsh-autosuggestions): autosuggestions for zsh
2. [forgit](https://github.com/wfxr/forgit): A utility tool powered by fzf for using git interactively
3. [yq](https://github.com/kislyuk/yq): jq wrapper for YAML/XML/TOML documents

**Tip of the week:** Make Zsh help more helpful

Zsh does not enable a builtin `help` command, instead it provides `run-help`. By default `run-help` is an alias to `man` and will only work on external commands. To use it for Zsh builtins and features, load and unalias the command in your `.zshrc`.

```sh
autoload -Uz run-help
unalias run-help
alias help=run-help # for convenience
```

For example, you can now run `help whence`, `help history`, etc.

---

`#cliday 2022-03-25`

1. [delta](https://github.com/dandavison/delta): A syntax-highlighting pager for git, diff, and grep output
2. [btop](https://github.com/aristocratos/btop): A monitor of resources
3. [zoxide](https://github.com/ajeetdsouza/zoxide): A smarter cd command

**Tip of the week:** Remove duplicate lines without sorting

If you have data with duplicate lines but don't want to change the order, try `awk '!a[$0]++'`! For example:

```sh
% cat << EOF > file1
Apple
Orange
Orange
Banana
Apple
Pineapple
EOF

% awk '!a[$0]++' file1
Apple
Orange
Banana
Pineapple
```

How does this work? You can read a wonderful walkthrough at [opensource.com](https://opensource.com/article/19/10/remove-duplicate-lines-files-awk).

---

`#cliday 2022-04-01`

1. [slides](https://github.com/maaslalani/slides): Terminal based presentation tool
2. [curlconverter](https://github.com/curlconverter/curlconverter): transpiles `curl` commands into programs in other programming languages
3. [trash-cli](https://github.com/sindresorhus/trash-cli): Move files and folders to the trash

**Tip of the week:** Merge two text files side-by-side with `paste`

For example:

```sh
% cat << EOF > file1
HEADER1
Data-1
Date-2
EOF

% cat << EOF > file2
HEADER2
Value-1
Value-2
EOF

% paste file1 file2
HEADER1 HEADER2
Data-1  Value-1
Date-2  Value-2
```
