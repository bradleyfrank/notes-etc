# Storage & Media Server

## Bootstrap

```sh
useradd --create-home --user-group --shell /bin/bash --comment "Ansible user" deploy > /dev/null
mkdir /home/deploy/.ssh > /dev/null && chmod 0700 /home/deploy/.ssh
cat << 'EOF' > /home/deploy/.ssh/authorized_keys
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIILk0WClzqNNs0JSgCXHuiWwi+j/ieldDCFc1JcMFfIU ansible-k8s-server
EOF
chown -R deploy:deploy /home/deploy/.ssh
cat << EOF > /etc/sudoers.d/00-deploy
deploy ALL=(ALL) NOPASSWD: ALL
EOF
```

## System Configs

### Networking

```bash
hostnamectl set-hostname deep-thought.francopuccini.casa
```

### SSH

```bash
sed -i \
  -e 's/^#PermitRootLogin prohibit-password/PermitRootLogin no/' \
  -e 's/^PasswordAuthentication yes/PasswordAuthentication no/' \
  /etc/ssh/sshd_config
# ssh-copy-id -i ~/.ssh/id_home.pub 192.168.1.40
systemctl restart sshd
```

### Firewall

```bash
ufw default allow outgoing ; ufw default deny incoming
ufw allow ssh && \
  ufw allow http && \
  ufw allow https && \
  ufw allow nfs && \
  ufw allow samba &&
ufw enable
ufw logging on
```

### Packages

```bash
apt upgrade -y
apt install -y \
  borgbackup \
  chrony \
  cifs-utils \
  ctop \
  git \
  glances \
  htop \
  linux-tools-generic \
  makepasswd \
  ncdu \
  nmap \
  pciutils \
  rename \
  samba \
  smartmontools \
  sshfs \
  ssmtp \
  strace \
  stow \
  toilet \
  trash-cli \
  tmux \
  unzip \
  vim \
  wget \
  zfsutils-linux \
  zfs-auto-snapshot
```

```bash
wget -P /usr/local/bin/ https://raw.githubusercontent.com/so-fancy/diff-so-fancy/master/third_party/build_fatpack/diff-so-fancy
chmod 755 /usr/local/bin/diff-so-fancy
```

### Time & Date

```bash
systemctl start chronyd
timedatectl set-timezone America/New_York
chronyc makestep
```

### Logging

```bash
sed -i 's/#Storage=auto/Storage=persistent/' /etc/systemd/journald.conf
systemctl restart systemd-journald.service

cat << EOF > /etc/logrotate.d/borg
/var/log/borg/*.log {
  rotate 4
  weekly
  compress
  missingok
  notifempty
}
EOF
```

### Mail

```bash
cat << EOF > /etc/ssmtp/ssmtp.conf
root=<email-address>
mailhub=<email-smtp:port>
hostname=<fqdn>
AuthUser=<email-username>
AuthPass=<email-password>
UseTLS=<YES|NO>
UseSTARTTLS=<YES|NO>
EOF
```

## Scripts & Composer Files

Checkout Git repo of scripts and composer files:

```bash
ssh-keygen -t rsa -b 4096 -N "" -C "$(uname -n)" -f /root/.ssh/id_rsa
# [add deploy key to GitHub repo]
mkdir /srv
git clone git@github.com:bradleyfrank/home-server.git /srv/home-server
```

Symlink scripts and cronjobs:

```bash
stow --no-folding --restow --dir /srv/home-server --target /usr/local/bin/ bin
stow --no-folding --restow --dir /srv/home-server --target /etc/ cron
```

## Data Structure

Remove any existing partitions from the target disks.

```bash
lsblk -o SIZE,TYPE,NAME -I 8 -d
parted -s /dev/sdX mklabel GPT
parted -s /dev/sdY mklabel GPT
...
parted -s /dev/sdN mklabel GPT
```

Get disk identifiers (see [Selecting /dev/ names when creating a pool](https://github.com/openzfs/zfs/wiki/faq#selecting-dev-names-when-creating-a-pool)):

```bash
ls -lh /dev/disk/by-id/ | grep sd[a-z]$
```

Create striped mirrored VDEVs:

```bash
zpool create -f nas0 \
  mirror \
    ata-Hitachi_HDS5C3020ALA632_ML4220F316DDPK \
    ata-Hitachi_HDS5C3020ALA632_ML4220F317KSSK \
  mirror \
    ata-HGST_HUS724040ALA640_PN1334PBJWZZGS \
    ata-HGST_HDN724040ALE640_PK2338P4H4Y7AC
```

Create the ZFS file systems:

```bash
# appdata
zfs create nas0/appdata
zfs create nas0/appdata/nextcloud
zfs create nas0/appdata/plex
zfs create nas0/appdata/jellyfin
zfs create nas0/appdata/traefik
# userdata
zfs create nas0/userdata
zfs create nas0/userdata/media
zfs create nas0/userdata/family
zfs create nas0/userdata/software
zfs create nas0/userdata/7030726e
# databases
zfs create nas0/db
zfs create nas0/db/nextcloud
# caches
zfs create nas0/cache
zfs create nas0/cache/transcode
zfs create nas0/cache/nextcloud
```

Configure ZFS snapshots:

```bash
# appdata
zfs set com.sun:auto-snapshot=true nas0/appdata
zfs set com.sun:auto-snapshot:monthly=true nas0/appdata
zfs set com.sun:auto-snapshot:weekly=true nas0/appdata
zfs set com.sun:auto-snapshot:daily=true nas0/appdata
zfs set com.sun:auto-snapshot:hourly=true nas0/appdata
zfs set com.sun:auto-snapshot:frequent=false nas0/appdata
# userdata
zfs set com.sun:auto-snapshot=true nas0/userdata
zfs set com.sun:auto-snapshot:monthly=true nas0/userdata
zfs set com.sun:auto-snapshot:weekly=true nas0/userdata
zfs set com.sun:auto-snapshot:daily=true nas0/userdata
zfs set com.sun:auto-snapshot:hourly=true nas0/userdata
zfs set com.sun:auto-snapshot:frequent=false nas0/userdata
# databases
zfs set com.sun:auto-snapshot=false nas0/db
# caches
zfs set com.sun:auto-snapshot=false nas0/cache
```

Configure Samba:

```bash
# Make generic user account to own file storage
groupadd --gid 10000 nasuser
useradd \
  --comment "Default NFS/SMB user" \
  --no-create-home \
  --shell /usr/sbin/nologin \
  --uid 10000 \
  --gid 10000 \
  nasuser

# Fix ownership on userdata shares
find /nas0/userdata -type d -exec chmod 2775 {} \;
chown -R nasuser:nasuser /nas0/userdata

# Create Samba shares config file
mkdir /etc/samba/smb.conf.d
cat << EOF > /etc/samba/smb.conf.d/user.conf
[7030726e]
  comment = 7030726e Media
  path = /nas0/userdata/7030726e
  browseable = no
  guest ok = yes
  read only = no
  force user = nasuser
  force create mode = 0775
  force directory mode = 2775

[media]
  comment = Media
  path = /nas0/userdata/media
  browseable = yes
  guest ok = yes
  read only = no
  force user = nasuser
  force create mode = 0775
  force directory mode = 2775

[software]
  comment = Software
  path = /nas0/userdata/software
  browseable = yes
  guest ok = yes
  read only = no
  force user = nasuser
  force create mode = 0775
  force directory mode = 2775

[family]
  comment = Family Media
  path = /nas0/userdata/family
  browseable = yes
  guest ok = yes
  read only = no
  force user = nasuser
  force create mode = 0775
  force directory mode = 2775
EOF

# Include the custom conf file in the main config file
echo -e "\ninclude = /etc/samba/smb.conf.d/user.conf" >> /etc/samba/smb.conf

# Restart services
systemctl restart smbd nmbd
```

## Containers

Install and run Docker:

```bash
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | apt-key add -
add-apt-repository \
 "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
apt install -y containerd.io docker-ce docker-ce-cli docker-compose
systemctl enable --now docker
```

Create internal Docker networks:

```bash
docker network create proxy
docker network create nextcloud
```

### Traefik

```bash
touch /srv/home-server/apps/traefik2/acme.json
chmod 0600 /srv/home-server/apps/traefik2/acme.json
cd /srv/home-server/apps/traefik2 && docker-compose up -d
```

### Nextcloud

```bash
cd /srv/home-server/apps/nextcloud && docker-compose up -d
# First run only, make Nextcloud aware of https proxy
sed -i \
  -e "/'overwrite.cli.url'/a \  'overwriteprotocol' => 'https'," \
  -e "s/'overwrite.cli.url' => 'http:/'overwrite.cli.url' => 'https:/" \
  /nas0/appdata/nextcloud/config/config.php
docker exec -it nextcloud service apache2 restart
```

Add the cronjob:

```bash
cd /etc/cron.d && ln -s /srv/home-server/apps/nextcloud/cron/nextcloud-background
```

### Plex

First run only:

1. Get Plex claim code: https://www.plex.tv/claim
2. Update `plex/docker-compose` with claim code

```bash
cd /srv/home-server/apps/plex && docker-compose up -d
```

### Watchtower

```bash
cd /srv/home-server/apps/watchtower && docker-compose up -d
```

## Backups

Initiate Borg repositories on remote host (i.e. Synology):

```bash
borg init \
  --encryption=repokey \
  --remote-path /usr/local/bin/borg \
  nas:/volume1/Backups/nas0/userdata
borg init \
  --encryption=repokey \
  --remote-path /usr/local/bin/borg \
  nas:/volume1/Backups/nas0/appdata/nextcloud
borg init \
  --encryption=repokey \
  --remote-path /usr/local/bin/borg \
  nas:/volume1/Backups/nas0/appdata/plex
```
