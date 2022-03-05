# Linux Management

## Package Management

```sh
# Red Hat Subscription Manager
subscription-manager clean
subscription-manager register --org=<org_id> --activationkey=<key_name> --force
subscription-manager config --rhsm.manage_repos=0
subscription-manager status

# firmware updates
sudo fwupdmgr get-updates
sudo fwupdmgr update

# remove snap packages and prevent snap installations
sudo apt install gnome-software
sudo apt remove gnome-software-plugin-snap
sudo apt remove --purge snapd
sudo apt-mark hold snap
sudo apt-mark hold snapd

# upgrade Fedora
sudo dnf upgrade --refresh
sudo dnf install dnf-plugin-system-upgrade
sudo dnf system-upgrade download --releasever=<version>
sudo dnf system-upgrade reboot
```

```sh
# List installed packages from specific repository:
yum repository-packages <repo> list installed

# Query available packages from specific repo:
yum --disablerepo="*" --enablerepo="<repo>" list available

# List services that require restarting:
needs-restarting | grep -E '^[0-9]+'

# Download packages to directory:
yum install -y --downloadonly <package> --downloaddir=/root/

# Find packages that need updating:
yum check-update
```

## Filesystems

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

# remove filesystem
wipefs -a /dev/device
```

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

```sh
mount -t nfs -o options server:/remote/export /local/directory
mount -o loop /path/to/image.iso /local/directory

# generate systemd filename
systemd-escape --path --suffix=mount /nfs/Media  # nfs-Media.mount
```

```sh
# create a CIFS password file
cat << EOF > /path/to/.cifs-auth
username=
password=
EOF
chmod 400 /path/to/.cifs-auth
```

## Firewall

```sh
systemctl enable --now firewalld
firewall-cmd --permanent --add-service=http --add-service=https --add-service=ssh
firewall-cmd --permanent --add-port=2222/tcp
firewall-cmd --reload
```

## Time Syncing

```sh
systemctl --now enable chronyd
timedatectl set-timezone America/New_York
chronyc makestep # step the system clock immediately

[watch] chronyc tracking # check status
chronyc sources [-v] # show time source configured in chrony.conf
```

## Cronjobs

```sh
run-parts --report --test /etc/cron.daily # test cronjobs
journalctl -u cron.service # view logs
```

Using `cron.d` files:

- No file extension
- File permissions `0755`
- Format: `M H DoM M DoW <user> <command>`

Using `cron.{hourly,weekly,monthly}` files:

- Exclude cron syntax
- Include shebang interpreter line

## SELinux

```sh
# show status
getenforce
getsebool [-a|$boolean]
sestatus

setenforce [enforcing|permissive] # enable/disable

semanage boolean -l # list all booleans
semanage boolean -m --off httpd_ssi_exec # enable/disable

semanage fcontext -l # list contexts
semanage fcontext -a -t sshd_key_t '/etc/ssh/keys(/.*)?'
restorecon -r /etc/ssh/keys

semanage port -l # list ports
semanage port -a -t http_cache_port_t -p tcp <port>
semanage port -a -t ssh_port_t -p tcp <port>
```

## Account Management

- `useradd` is the low-level command
- `adduser` can be a high-level utility that calls `useradd` or may be a symlink

```sh
# a generic user account to own file storage
groupadd --gid 10000 nasuser
useradd nasuser \
  --comment "Default NFS/SMB user" \
  --no-create-home \
  --shell "$(which nologin)" \
  --uid 10000 \
  --gid 10000

# a system account to own media files
adduser plex \
  --system \
  --user-group \
  --shell "$(which nologin)" \
  --home-dir /srv/plex \
  --no-create-home

# local account for the Gitea container to use
groupadd --gid 10100 git
useradd git \
  --comment "Gitea user for SSH" \
  --shell "$(which nologin)" \
  --create-home \
  --uid 10100 \
  --gid 10100
```

## Networking

```sh
# NetworkManager
nmcli con add type ethernet con-name main ifname em1 ip4 192.168.1.40/24 gw4 192.168.1.1
nmcli con mod main ipv4.dns "192.168.1.1 9.9.9.9 1.1.1.1"
nmcli con up main

# NetPlan
cat << EOF > /etc/netplan/00-static.yaml
network:
    version: 2
    ethernets:
        eno2:
            addresses:
            - 192.168.1.40/24
            gateway4: 192.168.1.1
            nameservers:
                addresses:
                - 192.168.1.1
                - 9.9.9.9
                - 1.1.1.1
                search:
                - domain.tld
EOF
netplan apply
```
