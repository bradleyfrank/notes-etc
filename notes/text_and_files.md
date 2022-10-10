# Text & Files

## Dates

```sh
# YYYY-MM-DDTHH:MM:SS-TZ
date --iso-8601=seconds

# filename safe date, e.g. 2020-05-11T085706-0400
date --iso-8601=seconds | tr -d ':'

# get datetime from external source
wget -qSO- --max-redirect=0 google.com 2>&1 | grep Date: | cut -d' ' -f5-9
```

## Fonts

```sh
# reload font cache
fc-cache -rf

# list font details
fc-list -v

# list all fonts with toilet
for font in *.tlf; do toilet --font ${font%%.*} ${font%%.*}; done
```

## Comparing

```sh
# produce a patch file
diff -Nur oldfile newfile > patchfile

# compare two directories
diff -q directory-1/ directory-2/

# compare two files
vimdiff file1 file2
code --diff file1 file2
sdiff -s file1 file2
comm -12 < (sort file1) < (sort file2)

# delete old duplicate images
fdupes --recurse --reverse --delete --noprompt .
```

## Files & Strings

```sh
# merge line-by-line
paste file1 file2 > file3

# skip first line in output
awk 'NR>1 {print $1}'

# split a file at every PATTERN
awk '/PATTERN/{f="newfile"++i;}{print > f;}'

# split file at every PATTERN but omit PATTERN
awk '/PATTERN/{f="newfile"++i;next}{print > f;}'

# split a file on every Nth line
awk 'NR%n==1{f="newfile"++i;}{print > f}'

# find non-adjacent unique lines
awk '!x[$0]++'

# increment version number
awk -vFS=. -vOFS=. '{$NF++;print}'

# insert at top of file
sed -i '1s/^/<added text> \n/'

# print all lines, inclusively, from search string
sed -n '/PATTERN/,$p'

# print all lines up to the match
sed '/PATTERN/q'

# delete all consecutive duplicate lines from a file
sed '$!N; /^\(.*\)\n\1$/!P; D'

# replace newlines with '\n'
sed ':a;N;$!ba;s/\n/\\n/g'
```

## Archiving

```sh
# extract initrd files
lz4 -d initrd.img initrd.cpio
mkdir initrd
cp initrd.cpio initrd/
cd initrd/
cpio -id < initrd.cpio
```
