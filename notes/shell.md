# Shell

```sh
f="path1/path2/file.ext"
len="${#f}"

# slicing: ${<var>:<start>} or ${<var>:<start>:<length>}
slice1="${f:6}"   # = "path2/file.ext"
slice2="${f:6:5}" # = "path2"
slice3="${f: -8}" # = "file.ext"

# splitting
extension="${f#*.}"       # = "ext"
filename="${f##*/}"       # = "file.ext"
filename="$(basename $f)" # = "file.ext"
dirname="${f%/*}"         # = "path1/path2"
dirname="$(dirname $f)"   # = "path1/path2"
root="${f%%/*}"           # = "path1"
```

---

```sh
echo $RANDOM # integer between 0 and 32767
echo $(( $RANDOM % 10 )) # random number 1-10
echo $SRANDOM # 32-bit pseudo-random number
```

---

```sh
$0   # name of the script
$n   # positional parameters to script/function
$$   # PID of the script
$!   # PID of the last command executed (and run in the background)
$?   # exit status of the last command
$#   # number of parameters to script/function
$@   # all parameters to script/function (sees arguments as separate word)
$*   # all parameters to script/function (sees arguments as single word)
```

---

```sh
# basic output to a file
cat << EOF > /path/to/file
The variable $foo will be interpreted.
EOF

# don't interpret variables
cat << 'EOF' > /path/to/file
The variable $bar will not be interpreted.
EOF

# pipe the heredoc through a command
cat << 'EOF' | sed 's/foo/bar/g' > /path/to/file
All instances of "foo" will be replaced.
EOF

# write the heredoc to a file using sudo
cat << 'EOF' | sudo tee /path/to/file
...
EOF
```

---

```sh
# Bash 4+ read file into array
mapfile -t foo < "file"
readarray -t foo < <( find . -name * )

# enter a password securely
read -r -s -p "Enter password: " my_password
```
