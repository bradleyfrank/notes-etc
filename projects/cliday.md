# `#cliday`

## 2022-03-18

1. `zsh` plugins:
    1. [zsh-syntax-highlighting](https://github.com/zsh-users/zsh-syntax-highlighting): syntax highlighting for Zsh
    2. [zsh-autosuggestions](https://github.com/zsh-users/zsh-autosuggestions): autosuggestions for zsh
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

## 2022-03-25

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

## 2022-04-01

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

## 2022-04-08

1. [tealdeer](https://github.com/dbrgn/tealdeer): A very fast implementation of tldr in Rust
2. [prettyping](https://github.com/denilsonsa/prettyping): A wrapper around the standard `ping` tool, making the output prettier, more colorful, more compact, and easier to read
3. [onefetch](https://github.com/o2sh/onefetch): Git repository summary on your terminal

**Tip of the week:** Easily insert a blank line between concatenated files

For example:

```sh
% printf "1: file ending with no newline" > 1.txt
% echo "2: file ending with a newline" > 2.txt

% cat *.txt
1: file ending with no newline2: file ending with a newline

% awk 'FNR==1{print ""}1' *.txt

1: file ending with no newline

2: file ending with a newline

% awk 'FNR==2{print ""}1' *.txt
1: file ending with no newline
2: file ending with a newline
```

## 2022-04-15

1. [bandwhich](https://github.com/imsnif/bandwhich): Terminal bandwidth utilization tool
2. [redo](https://github.com/barthr/redo): Create reusable functions from your history in an interactive way
3. [usql](https://github.com/xo/usql): Universal command-line interface for SQL databases

**Tip of the week:** Convert plist files on macOS to other formats with `plutil`:

For example:

```sh
# From binary format to json or xml:
plutil -convert json ~/Library/Preferences/com.google.Chrome.plist -o ~/com.google.Chrome.json
plutil -convert xml1 ~/Library/Preferences/com.google.Chrome.plist -o ~/com.google.Chrome.xml

# Back to binary format:
plutil -convert binary1 ~/com.google.Chrome.xml -e plist
```

## 2022-04-22

1. [mkcert](https://github.com/FiloSottile/mkcert): Make locally trusted development certificates with any names you'd like
2. [procs](https://github.com/dalance/procs): A modern replacement for ps written in Rust
3. [ripgrep](https://github.com/BurntSushi/ripgrep): Recursively searches directories for a regex pattern while respecting your gitignore

**Tip of the week:** Use `awk` to increment a semantic version number

Split the string by a period character, and `$NF` will represent the last segment of the version number. The output field separator is also set to a period character so the return string is in semver format. For example:

```sh
% echo "3.6" | awk -v FS=. -v OFS=. '{$NF++;print}'
3.7

% echo "3.6.13" | awk -v FS=. -v OFS=. '{$NF++;print}'
3.6.14

% echo "3.6.13" | awk -v FS=. -v OFS=. '{$(NF-1)++;print}'
3.7.13

% echo "3.6.13" | awk -F. '{$(NF-2)++;print $1}'
4
```

## 2022-04-29

1. [file-arranger](https://github.com/anhsirk0/file-arranger): Simple & capable File/Directory arranger/cleaner
2. [dust](https://github.com/bootandy/dust): A more intuitive version of du in rust
3. [atuin](https://github.com/ellie/atuin): Magical shell history

**Tip of the week:** Use `openssl` for quick-and-dirty file encryption

Example:

```sh
% echo "My plaintext file." > /tmp/file1.txt

# Using the default macOS LibreSSL (results in a binary file):
% openssl enc -aes-256-cbc -salt -in /tmp/file1.txt -out /tmp/file1.enc
% openssl enc -d -aes-256-cbc -in /tmp/file1.enc -out /tmp/file1.txt

# Using OpenSSL from Homebrew (results in a more secure, base64 text file):
% /usr/local/opt/openssl@3/bin/openssl enc -pbkdf2 -iter 100000 -aes256 -salt -base64 \
  -in /tmp/file1.txt -out /tmp/file1.enc
% /usr/local/opt/openssl@3/bin/openssl enc -d -pbkdf2 -iter 100000 -aes256 -base64 \
  -in /tmp/file1.enc -out /tmp/file1.txt
```

## 2022-05-06

1. [git-sweep](https://github.com/arc90/git-sweep): Clean up Git branches that have been merged into master
2. [bat](https://github.com/sharkdp/bat): A cat(1) clone with wings
3. [rdfind](https://github.com/pauldreik/rdfind): find duplicate files utility

**Tip of the week:** You can avoid manually working with temp files by using ZSH process substitution:

Example:

```sh
% echo "Banana\nApple\nCucumber" > /path/to/file1
% sort /path/to/file1 > /path/to/file1 # Fails!

# Solution with a temp file:
% temp1=$(mktemp)
% sort /path/to/file1 > "$temp1"
% mv "$temp1" /path/to/file1

# Solution with process substitution:
% mv =(sort /path/to/file1) /path/to/file1
```

## 2022-05-13

1. [tablemark-cli](https://github.com/haltcase/tablemark-cli): Generate markdown tables from JSON data
2. [gh-cli](https://github.com/cli/cli): GitHub’s official command line tool
3. [bandwhich](https://github.com/imsnif/bandwhich): Terminal bandwidth utilization tool

**Tip of the week:** Quickly retrieve a deleted file from a Git repository:

```sh
% file="./repo/path/to/file"
git checkout $(git rev-list -n 1 HEAD -- "$file")~1 -- "$file"
```

Don't know the full path of the file?

```sh
% filename="filename"
% sha="$(git log --all --full-history -1 --format=%H -- "**/$filename.*")" && \
  git checkout "$sha"~1 -- "$(git diff-tree --no-commit-id --name-only -r "$sha" | grep "$filename")"
```

## 2022-05-20

1. [exa](https://github.com/ogham/exa): A modern replacement for `ls`
2. [buku](https://github.com/jarun/buku): Personal mini-web in text
3. [treeage](https://github.com/Kraymer/treeage): Listing contents of repository in a tree-like format with age metric

**Tip of the week:** Move around directories quickly with various Zsh builtin methods:

```sh
# Return immediately to the previous directory:
% cd -

# With zsh, enable auto_cd [in ~/.zshrc] to move around without `cd`:
% setopt auto_cd
% .. # Go up a directory
% ../foo # Go up a directory and enter the 'foo' directory
% ../.. # Go up two directories

# Set a "bookmarked" directory once auto_cd is enabled:
% cdpath=(/path/to/important_directory)
% cd important_directory/subdirectory

# Keep a running list of directories visited:
% setopt auto_pushd
% cd /usr/local/bin; cd ~/.local/bin; cd ~/.config/gcloud
% echo $dirstack # See your directory stack
% cd -2 # Jump to element '2' in the stack (counting from the right, starting at zero)
% cd +1 # Jump to element '1' in the stack (counting from the left, starting at zero)

# Now the fun begins:
% setopt pushd_ignore_dups # Prevent duplicates in the stack
% cd "$(printf '%s\n' "${dirstack[@]}" | fzf)"
```

## 2022-05-27

1. [lazydocker](https://github.com/jesseduffield/lazydocker): The lazier way to manage everything docker
2. [fzf](https://github.com/junegunn/fzf): A command-line fuzzy finder
3. [git-xargs](https://github.com/gruntwork-io/git-xargs): Make updates across multiple Github repositories with a single command

**Tip of the week:** How to make a loading animation:

```sh
frames="/ | \\ -"
while :; do
  for f in $frames; do printf "\r%s Loading..." "$f"; sleep 0.5; done
done
```

## 2022-06-03

1. [fd](https://github.com/sharkdp/fd): A simple, fast and user-friendly alternative to 'find'
2. [bandwhich](https://github.com/imsnif/bandwhich): Terminal bandwidth utilization tool
3. [fileicon](https://github.com/mklement0/fileicon): macOS CLI for managing custom icons for files and folders

**Tip of the week:** How to batch install Homebrew packages for a quick bootstrap:

```sh
# On the existing system, dump all installed packages (taps, formulas, casks, and app store):
% brew bundle dump
# This creates a 'Brewfile' in the current directory:
% cat Brewfile
# Copy this file to a new system and run:
% brew bundle install
# To keep your system up-to-date using this method check out:
% brew bundle --help
# Pair this with `stow` to quickly install dotfiles and get a new system running in no time!
```

## 2022-06-10

1. [dog](https://github.com/ogham/dog): A command-line DNS client
2. [tmuxp](https://github.com/tmux-python/tmuxp): tmux session manager

**Article of the week:** [6 deprecated Linux commands and the tools you should be using instead](https://www.redhat.com/sysadmin/deprecated-linux-command-replacements)

> This article shares a handful of older tools that you might be still using, what you should be using instead, and why you should switch to these improved alternatives that provide the same functionality, if not more.

**Tip of the week:** Use Python as a simple `jq` replacement:

```sh
foo='{"cities": {"boston": "ma", "miami": "fl", "seattle": "wa"}}'
python -c "import sys, json;print(json.loads(sys.stdin.read())['cities']['seattle'])" <<< "$foo"
# Bonus: use `jo` to create json:
foo="$(jo -p cities=$(jo boston=ma miami=fl seattle=wa))"
```
