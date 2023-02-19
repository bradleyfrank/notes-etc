# Notes

## Ansible

```sh
# encrypt file with existing password
ansible-vault encrypt --vault-id /path/to/password <file>
ansible-vault encrypt_string --stdin-name <variable_name>
```

## Color Schemes

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

## Document and Image Conversion

```sh
pandoc file.md -f gfm -t dokuwiki -o file.wiki  # convert GitHub Markdown to DokuWiki format
qpdf --password="PASSWORD" --decrypt input.pdf output.pdf  # remove password from PDF
pdftk /path/to/input.pdf input_pw PROMPT output /path/to/output.pdf  # remove password from PDF
penssl enc -aes-256-cbc -salt -in /path/to/input -out /path/to/output  # encrypt file
openssl enc -d -aes-256-cbc -in /path/to/input -out /path/to/output  # decrypt file
soffice --headless --convert-to docx --outdir /tmp /path/to/doc  # convert doc to docx
libreoffice --headless --convert-to epub /path/to/odt  # convert odt to epub
convert /path/to/file -resize 50% /path/to/output  # resize image by 50%
convert -coalesce file.gif out.png  # extract gif images
heif-convert "$f" ${f/%.HEIC/.JPG}  # convert HEIC images
ffmpeg -i "$f" "${f%.webp}.jpg"  # convert webp images
```

## Files and Strings

### Comparing

```sh
fdupes --recurse --reverse --delete --noprompt .  # delete old duplicate images
diff -Nur oldfile newfile > patchfile  # produce a patch file
diff -q directory-1/ directory-2/  # compare two directories

# compare two files
vimdiff file1 file2
code --diff file1 file2
sdiff -s file1 file2
comm -12 < (sort file1) < (sort file2)
```

### Matching

```sh
paste file1 file2 > file3  # merge line-by-line
awk 'NR>1 {print $1}'  # skip first line in output
awk '/PATTERN/{f="newfile"++i;}{print > f;}'  # split a file at every PATTERN
awk '/PATTERN/{f="newfile"++i;next}{print > f;}'  # split file at every PATTERN but omit PATTERN
awk 'NR%n==1{f="newfile"++i;}{print > f}'  # split a file on every Nth line
awk '!x[$0]++'  # find non-adjacent unique lines
awk -vFS=. -vOFS=. '{$NF++;print}'  # increment version number
sed -i '1s/^/<added text> \n/'  # insert at top of file
sed -n '/PATTERN/,$p'  # print all lines, inclusively, from search string
sed '/PATTERN/q'  # print all lines up to the match
sed '$!N; /^\(.*\)\n\1$/!P; D'  # delete all consecutive duplicate lines from a file
sed ':a;N;$!ba;s/\n/\\n/g'  # replace newlines with '\n'
```

## Git

```sh
# clone by tag
git clone -b <tagname> <repository> .

# logs and searching
git log --full-history -- /path/to/file  # search for file changes
git log --all --grep='Build 0051'  # search the commit log (across all branches) for the given text
git grep 'Build 0051' $(git rev-list --all)  # search the content of commits

# find and retrieve a deleted file
file=/path/to/file
git checkout $(git rev-list -n 1 HEAD -- "$file")~1 -- "$file"

# find commiter and show commit
git log --format='%h %ae' | grep {{ email }} | awk '{print $1}' | xargs git show

# branching
git push --delete <remote_name> <branch_name>  # delete remote branch
git branch -d <branch_name>  # delete local branch
git branch –m <new_name>  # rename local branch
git push origin -u <new_name>  # rename remote branch
git push origin --delete <old_name>  # delete old branch

# comparing
git diff --staged  # diff files already staged
git diff --stat  # diff summary
git diff --check  # check for conflicts and whitespace errors

# fixups
git reset --hard [HEAD|<hash>]  # forget all the changes, clean start
git reset <hash>  # edit, re-stage and re-commit files
git reset --soft <hash>  # re-commit past commits, as one big commit

# submodules
git clone --recursive --jobs {{ int }} {{ repo }}  # clone repo w/ submodules (synchronously)
git submodule update --init  # load submodules in a previously cloned repo
git submodule update --init --recursive  # for nested submodules
git submodule update --init --recursive --jobs 8  # " " " (synchronously)
git submodule update --remote  # pull all changes in submodules
git submodule add <repo>  # add a child repository to a parent repository
git submodule init  # initialize an existing Git submodule
git submodule update  # update the commit of the submodule to the latest commit
```

### Commit Signing

```sh
ssh-keygen -t rsa -b 4096 -C "me@email.com"
git config --global user.name "Name"
git config --global user.email "me@email.com"
git config --global user.signingkey "$(cat ~/.ssh/id_rsa.pub)"
git config --global commit.gpgsign true
git config --global gpg.format ssh
git config --global gpg.ssh.allowedSignersFile "$HOME/.ssh/allowed_signers"
printf "<email> %s" "$(awk '{print $1" "$2}' /path/to/public/key)" >> ~/.ssh/allowed_signers
```

## GitHub API

```sh
gh api search/repositories\?q=org:<org>+language:<language>
gh api search/issues\?q=repo:<org>/<repo>+is:pr+is:merged
gh api search/issues\?q=repo:<org>/<repo>+is:pr+is:merged+merged:\>=<YYYY-MM-DD>
gh api search/repositories\?q=org:<org>+language:<language> | jq ' .items | .[] | .name'
gh api -X PATCH /repos/<org>/<repo> -f archived=true

# GET GitHub Gist
curl --fail --silent \
  --header "Accept: application/vnd.github.v3+json" \
  --header "Authorization: token <token>" \
  https://api.github.com/gists/<id>

# PATCH GitHub Gist
curl --fail --silent \
  --header "Accept: application/vnd.github.v3+json" \
  --header "Authorization: token <token>" \
  --request PATCH https://api.github.com/gists/<id> \
  --data "{\"files\": { \"filename\": { \"content\": \"...\" }}}"

# POST GitHub Gist
curl --fail --silent \
  --header "Accept: application/vnd.github.v3+json" \
  --header "Authorization: token <token>" \
  --request POST https://api.github.com/gists \
  --data "{\"files\": { \"cmarks\": { \"content\": \"...\" }}}"
```

## Google Cloud

```sh
# get configs
gcloud projects describe $(gcloud config list --format 'value(core.project)') --format 'value(name)'
gcloud projects describe $(gcloud config get-value project) --format 'value(name)'
gcloud info --format='value(config.paths.active_config_path)'
gcloud info --format='value(config.paths.sdk_root)'
gcloud config configurations list --filter='is_active=True' --format='value(name)'

# service accounts
gcloud iam service-accounts update {{ sa }} \
  --display-name "..." --description "..."  # update the description and the display name
gcloud iam service-accounts get-iam-policy {{ sa }}  # check the IAM policy for sa
gcloud iam service-accounts add-iam-policy-binding {{ sa }} \
  --member {{ email }} --role roles/{{ role }}  # add a user to the policy
```

## Kubernetes

```sh
kubectl get pods -selector=app=<app>
kubectl patch pod <pod> -p '{"metadata":{"finalizers":null}}'   # remove finalizer
kubectl delete --wait=false pod <pod> --grace-period=<seconds>  # terminate gracefully
kubectl delete --grace-period=1 pod <pod>                       # terminate immediately
kubectl delete --grace-period=0 pod <pod> --force=true          # terminate forced
kubectl scale --replicas=3 deployment <deployment>              # scale deployment replicas
kubectl rollout history deployment <deployment> [--revision=<num>]
kubectl cordon <node>    # schedule
kubectl uncordon <node>  # unschedule
kubectl get secret <secret> -o json \
  | jq -r '.data."tls.crt"' \
  | base64 --decode \
  | openssl x509 -noout -enddate  # verify certificate
kubectl proxy --port=8001 && curl http://localhost:8001/api/v1/namespace/default/pods  # proxy
kubectl port-forward <pod> <port>  # port-forward
kubectl top <pods|nodes> --sort-by=<memory|cpu>
```

## Linux

```sh
# extract initrd files
lz4 -d initrd.img initrd.cpio
mkdir initrd
cp initrd.cpio initrd/
cd initrd/
cpio -id < initrd.cpio
```

### cron

```sh
run-parts --report --test /etc/cron.daily  # test cronjobs
```

### Desktop

```sh
gvfs-mime --set x-scheme-handler/https google-chrome.desktop  # set default app

# show desktop session (wayland/x11)
loginctl show-session $(awk '/tty/ {print $1}' <(loginctl)) -p Type | awk -F= '{print $2}'
echo $XDG_SESSION_TYPE

# nVidia "night mode" fix for Linux
cat << EOL >> /etc/X11/xorg.conf.d/20-nvidia.conf
Section "Device"
  Option "UseNvKmsCompositionPipeline" "false"
EndSection
EOL
```

### Filesystems

```sh
parted -s /dev/sdX mklabel GPT  # new partition table
parted -s /dev/sdX mkpart primary 1M 100%  # ensures partition is properly aligned (1M = 2048s)
parted -s /dev/sdX set 1 [raid|lvm] on  # mark partition for raid (mdadm) or lvm

mdadm -Cv /dev/md/<name> /dev/sdX1 /dev/sdY1 --level=1 --raid-devices=2  # create new array

pvcreate /path/to/device  # create physical volume on array or disk partition
vgcreate <vg> /dev/md/<name>  # create volume group
lvcreate -L <num>G -n <lv> <vg>  # create logical volume with specific size
lvcreate -l 100%FREE -n <lv> <vg>  # create logical volume with percent size
vgextend <vg> /path/to/disk  # extend volume group
lvextend -L +<num>G /dev/mapper/<lv>  # extend logical volume

mkfs -t xfs -n ftype=1 /path/to/volume  # format for Docker
mkfs -t xfs /dev/mapper/<vg>-<lv>  # format logical volume

# extend & grow
resize2fs /dev/device
xfs_growfs /dev/device

# repair filesystem
xfs_repair -L /dev/device

# remove filesystem
wipefs -a /dev/device
```

#### ZFS

```sh
zpool create -f tank \
  mirror \
    ata-Hitachi_HDS5C3020ALA632_ML4220F316DDPK \
    ata-Hitachi_HDS5C3020ALA632_ML4220F317KSSK \
  mirror \
    ata-HGST_HUS724040ALA640_PN1334PBJWZZGS \
    ata-HGST_HDN724040ALE640_PK2338P4H4Y7AC

zfs create tank/parent1 [-m /path/to/mountpoint -o quota=<num>G]
zfs create tank/parent1/child1

zpool list
zpool status
```

### Firewall

```sh
systemctl enable --now firewalld
firewall-cmd --permanent --add-service=http --add-service=https --add-service=ssh
firewall-cmd --permanent --add-port=2222/tcp
firewall-cmd --reload
```

### Mounts

```sh
mount -t nfs -o options server:/remote/export /local/directory
mount -o loop /path/to/image.iso /local/directory
systemd-escape --path --suffix=mount /nfs/Media  # nfs-Media.mount
```

### Networking

```sh
# find ip address
ip -4 -o addr show | grep -Ev '\blo\b' | grep -Po 'inet \K[\d.]+'
ip -4 -o addr show | grep -Po 'inet \K[\d.]+'
```

### Package Management

```sh
yum repository-packages <repo> list installed  # list installed pkgs from repo
yum --disablerepo="*" --enablerepo="<repo>" list available  # query available pkgs from repo
needs-restarting | grep -E '^[0-9]+'  # list services that need restarting
yum install -y --downloadonly <package> --downloaddir=/root/  # download pkgs to directory
yum check-update  # list pkgs that need updating

# Red Hat Subscription Manager
subscription-manager clean
subscription-manager register --org=<org_id> --activationkey=<key_name> --force
subscription-manager config --rhsm.manage_repos=0
subscription-manager status

# firmware updates
fwupdmgr get-updates
fwupdmgr update

# remove snap packages and prevent snap installations
apt-get install gnome-software
apt-get remove gnome-software-plugin-snap
apt-get remove --purge snapd
apt-mark hold snap
apt-mark hold snapd

# upgrade Fedora
dnf upgrade --refresh
dnf install dnf-plugin-system-upgrade
dnf system-upgrade download --releasever=<version>
dnf system-upgrade reboot
```

### SELinux

```sh
getenforce  # show status
getsebool [-a|$boolean]
sestatus

setenforce [enforcing|permissive]  # enable/disable
semanage boolean -l  # list all booleans
semanage boolean -m --off httpd_ssi_exec  # enable/disable
semanage fcontext -l  # list contexts
semanage fcontext -a -t sshd_key_t '/etc/ssh/keys(/.*)?'
restorecon -r /etc/ssh/keys
semanage port -l  # list ports
semanage port -a -t http_cache_port_t -p tcp <port>
semanage port -a -t ssh_port_t -p tcp <port>
```

## macOS

```sh
# system information
systemstats
system_profiler
sw_vers

# set hostname
sudo scutil --set HostName "hostname.local"
sudo scutil --set LocalHostName "hostname"
sudo scutil --set ComputerName "hostname"
sudo dscacheutil -flushcache

sudo nvram AutoBoot=%00  # disable auto-boot on keypress
pmset -g batt | grep -E 'InternalBattery' | cut -f2 | awk -F\; '{print $1$2}'  # get battery
osascript -e 'tell application "Safari" to add reading list item "<url>"'
sudo softwareupdate -aiR  # install macOS updates and reboot
printf "%s ALL=(ALL) NOPASSWD: ALL\n" "$(id -un)" \
  | sudo VISUAL="tee" visudo -f /etc/sudoers.d/nopasswd  # add entries to '/etc/sudoers.d'
```

### Homebrew

```sh
brew bundle dump  # write a Brewfile
brew bundle cleanup --force  # uninstall all dependencies not listed in Brewfile
brew info alacritty --cask --json=v2 | jq -r '.casks[].version'   # get cask version
brew info toilet --json=v2 | jq -r '.formulae[].versions.stable'  # get formulae version
brew info google-cloud-sdk --json=v2 \
  | jq -r '.casks[].installed,.formulae[].installed[].version'    # get install status
```

## Network Testing

```sh
nc -zw1 ports.ubuntu.com 80  # test website/port

# get Apache web server status
curl -Is --max-time 5 https://<domain>/server-status | head -n 1

# capture packets
tcpdump --list-interfaces
tcpdump -i eth0
tcpdump -w my_packet_capture.pcap
```

## Nextcloud

```sh
# scan entire directory for new files
docker exec --user www-data nextcloud php occ files:scan --all

# scan specific directory for new files
docker exec nextcloud php occ files:scan --user www-data --path="path/to/dir"
```

## Shell

```sh
cat << EOF > /path/to/file  # variables will be interpreted
cat << 'EOF' > /path/to/file  # variables will not be interpreted
cat << 'EOF' | sed 's/foo/bar/g' > /path/to/file  # replace 'foo' with 'bar'
cat << 'EOF' | sudo tee /path/to/file  # write to file using sudo

read -rsp "Enter password: " my_password  # enter a password securely

# read file into array (Bash 4+)
mapfile -t foo < "file"
readarray -t foo < <( find . -name * )

# substrings: ${<var>:<start>} or ${<var>:<start>:<length>}
foo="substring example"
echo ${foo:5:5}  # ring
echo ${foo:3}    # string example
echo ${foo:0:-3} # substring exam

bar="path1/path2/file.ext"
echo "${bar#*.}"   # ext
echo "${bar##*/}"  # file.ext
echo "${bar%/*}"   # path1/path2
echo "${bar%%/*}"  # path1
```

## SSH

```sh
ssh-keygen -yf /path/to/private/key  # restore a public key
ssh-keygen -lf /path/to/private/key  # verify key
ssh-keygen -R <hostname> -f ~/.ssh/known_hosts  # remove host
ssh-copy-id  # install public key in server's authorized_keys file

# start ssh agent
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_rsa

# tunnel a remote port available via the proxy; i.e. remote = DB and proxy = bastion
ssh -M -S <ctl_path> -fNL <local_port>:<remote_host>:<remote_port> <proxy_host>
ssh -S <ctl_path> -O check <proxy_host>  # check status of tunnel
ssh -S <ctl_path> -O exit <proxy_host>  # close the tunnel

# tunnel a port from local system through ssh connection
ssh -R <remote_port>:localhost:<local_port> <remote_host>
```

```sh
# automatically rsync dotfiles to remote host (%d = home directory)
Match Host 192.168.123.*,another-example.org,*.example.com User myusername,myotherusername
  ForwardAgent yes
  PermitLocalCommand yes
  LocalCommand rsync -L --exclude <dir1|file1> --exclude <dir2|file2>  -vRrlptze "ssh -o PermitLocalCommand=no" %d/./.gitignore %d/./.ssh/git_ed25519.pub %d/./.ssh/authorized_keys %d/./.vimrc %d/./.zshrc %d/./.config/iterm2/ %d/./.vim/ %d/./bin/ %d/./.bash/ %r@%n:/home/%r
```

## tmux

```
# create a shared session
tmux -S /tmp/shared new -s shared
sudo chgrp google-sudoers /tmp/shared
sudo chmod 775 /tmp/shared
# ...
tmux -S /tmp/shared attach -t shared
```

## Video Ripping and Transcoding

```sh
sudo docker pull ntodd/video-transcoding
sudo docker run -itv "$PWD":/data ntodd/video-transcoding
transcode-video --scan ./
transcode-video --encoder x265 -o movie.mkv ./  # transcode feature title to h265 mkv
transcode-video --encoder x265 --title <title> -o title.mkv ./  # transcode a title to h265 mkv

flac -cd "$f" | lame -b 192 - "${f%.*}.mp3"     # flac to mp3
ffmpeg -i "$f" -b:a 192K -vn "${f%.*}.mp3"      # mp4 to mp3
ffmpeg -i "$f" -c:a alac "${f%.*}.m4a"          # flac to m4a
ffmpeg -i "$f" -f flac "${f%.*}.flac" -vsync 0  # m4a to flac
ffmpeg -i input.mpg output.mp4                  # mpg to mp4
ffmpeg -i input.mp4 -vcodec libx264 -crf {18..24} output.mp4
ffmpeg -i input.mp4 -vcodec libx265 -crf {24..30} output.mp4
ffmpeg -protocol_whitelist file,http,https,tcp,tls,crypto -i "$f" -c copy \
  -bsf:a aac_adtstoasc "${f%.*}.mp4"            # m3u8 to mp4

makemkvcon backup --decrypt disc:0 /path/to/folder  # rip blu-ray as decrypted backup
makemkvcon mkv disc:0 all /path/to/folder           # rip blu-ray as mkv
makemkvcon mkv iso:/path/to/file.iso all /path/to/output                 # convert ISO to mkv
mkvmerge -o outfile.mkv infile_01.mp4 \+ infile_02.mp4 \+ infile_03.mp4  # merge mp4/mkv files
```

## Vim

```sh
" use hybrid line numbering by default with automatic toggling
augroup numbertoggle
  autocmd!
  autocmd BufEnter,FocusGained,InsertLeave * set relativenumber
  autocmd BufLeave,FocusLost,InsertEnter   * set norelativenumber
augroup END

" Change directory to the current buffer when opening files.
set autochdir
```

## zsh

```sh
setopt transient_rprompt  # show zsh right prompt only on active prompt
%(5~|%-1~/.../%3~|%~)  # truncate to 1st and last 3 segments if longer than 5
```

