# Command Line

```sh
# YYYY-MM-DDTHH:MM:SS-TZ
date --iso-8601=seconds

# filename safe date, e.g. 2020-05-11T085706-0400
date --iso-8601=seconds | tr -d ':'

# get datetime from external source
wget -qSO- --max-redirect=0 google.com 2>&1 | grep Date: | cut -d' ' -f5-9
```

---

```sh
# set default app
gvfs-mime --set x-scheme-handler/https google-chrome.desktop

# reload font cache
fc-cache -rf

# list font details
fc-list -v

# show desktop session (wayland/x11)
loginctl show-session $(awk '/tty/ {print $1}' <(loginctl)) -p Type | awk -F= '{print $2}'
echo $XDG_SESSION_TYPE

# list all fonts with toilet
for font in *.tlf; do toilet --font ${font%%.*} ${font%%.*}; done
```

---

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

---

```sh
# merge line-by-line
paste file1 file2 > file3

# skip first line in output
awk 'NR>1 {print $1}'

# split a file at every occurrence of PATTERN
awk '/PATTERN/{f="newfile"++i;}{print > f;}'

# split file at every occurrence of PATTERN but omit PATTERN from new file
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
sed -n '/foo/,$p'

# print all lines up to the match
sed '/PATTERN/q'

# delete all consecutive duplicate lines from a file
sed '$!N; /^\(.*\)\n\1$/!P; D'

# grep for a string, pipe to sed to replace text
grep -lr "string1" path/to/files/ | xargs sed -i 's/string1/string2/g'
```

---

```sh
# inline, no headers, multi
fzf --multi --ansi -i -1 --height=50% --reverse -0 --inline-info --border rounded

# inline, no headers, no multi
fzf --no-multi --ansi -i -1 --height=50% --reverse -0 --inline-info --border rounded

# inline, headers, multi
fzf --multi --ansi -i -1 --height=50% --reverse -0 --header-lines=1 --inline-info --border rounded
```

---

```sh
# extract initrd files
lz4 -d initrd.img initrd.cpio
mkdir initrd
cp initrd.cpio initrd/
cd initrd/
cpio -id < initrd.cpio
```

---

```sh
# convert GitHub Markdown to DokuWiki format
pandoc file.md -f gfm -t dokuwiki -o file.wiki

# remove password from PDF
pdftk /path/to/input.pdf input_pw PROMPT output /path/to/output.pdf

# encrypt/decrypt a file
openssl enc -aes-256-cbc -salt -in /path/to/input -out /path/to/output
openssl enc -d -aes-256-cbc -in /path/to/input -out /path/to/output

# converting documents with LibreOffice
soffice --headless --convert-to docx --outdir /tmp /path/to/doc
libreoffice --headless --convert-to epub /path/to/odt

# resize image by 50%
convert /path/to/file -resize 50% /path/to/output

# extract gif images
convert -coalesce file.gif out.png

# convert HEIC images
heif-convert "$f" ${f/%.HEIC/.JPG}

# convert webp images
ffmpeg -i "$f" "${f%.webp}.jpg"

# flac to mp3
flac -cd "$f" | lame -b 192 - "${f%.*}.mp3"

# mp4 to mp3
ffmpeg -i "$f" -b:a 192K -vn "${f%.*}.mp3"

# flac to m4a
ffmpeg -i "$f" -c:a alac "${f%.*}.m4a"

# m4a to flac
ffmpeg -i "$f" -f flac "${f%.*}.flac" -vsync 0

# mpg to mp4
ffmpeg -i input.mpg output.mp4
ffmpeg -i input.mp4 -vcodec libx264 -crf {18..24} output.mp4
ffmpeg -i input.mp4 -vcodec libx265 -crf {24..30} output.mp4

# m3u8 to mp4
ffmpeg -protocol_whitelist file,http,https,tcp,tls,crypto -i "$f" -c copy -bsf:a aac_adtstoasc "${f%.*}.mp4"
```

---

```sh
# rip blu-ray as decrypted backup
makemkvcon backup --decrypt disc:0 /path/to/folder

# rip blu-ray as mkv
makemkvcon mkv disc:0 all /path/to/folder

# convert ISO to mkv
makemkvcon mkv iso:/path/to/file.iso all /path/to/output

# merge mp4/mkv files
mkvmerge -o outfile.mkv infile_01.mp4 \+ infile_02.mp4 \+ infile_03.mp4
```

---

```sh
# test website/port
nc -zw1 ports.ubuntu.com 80

# find ip address
ip -4 -o addr show | grep -Ev '\blo\b' | grep -Po 'inet \K[\d.]+'
ip -4 -o addr show | grep -Po 'inet \K[\d.]+'

# get Apache web server status
curl -Is --max-time 5 https://<domain>/server-status | head -n 1

# capture packets
tcpdump --list-interfaces
tcpdump -i eth0
tcpdump -w my_packet_capture.pcap
```

---

```sh
# encrypt file with existing password
ansible-vault encrypt --vault-id /path/to/password <file>
ansible-vault encrypt_string --stdin-name <variable_name>
```

---

```sh
openssl rsa -text -noout -in /path/to/private/key # show key info
ssh-keygen -yf /path/to/private/key # restore a public key
ssh-keygen -lf /path/to/private/key # verify key
ssh-keygen -R <hostname> -f ~/.ssh/known_hosts # remove host
ssh-copy-id # install public key in server's authorized_keys file

# tunnel a remote port available via the proxy; i.e. remote = DB and proxy = bastion
ssh -M -S <ctl_path> -fNL <local_port>:<remote_host>:<remote_port> <proxy_host>
ssh -S <ctl_path> -O check <proxy_host> # check status of tunnel
ssh -S <ctl_path> -O exit <proxy_host> # close the tunnel

# tunnel a port from your local system through your ssh connection
ssh -R <remote_port>:localhost:<local_port> <remote_host>
```

---

```sh
gpg --full-generate-key
gpg --export --armor <email>
gpg --list-secret-keys --keyid-format=long
gpg --armor --export <key_id>
```
