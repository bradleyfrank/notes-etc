# Kubernetes Server

```sh
useradd --create-home --user-group --shell /bin/bash --comment "Ansible user" deploy > /dev/null

mkdir /home/{bfrank,deploy}/.ssh > /dev/null && chmod 0700 /home/{bfrank,deploy}/.ssh

cat << EOF > /home/bfrank/.ssh/authorized_keys
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIFStPMEL6J3I60LhF5HpzGdfv3eJymi3UKVDWPq7VOjP bfrank@francopuccini.casa
EOF

chown -R bfrank:bfrank /home/bfrank/.ssh

cat << 'EOF' > /home/deploy/.ssh/authorized_keys
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIILk0WClzqNNs0JSgCXHuiWwi+j/ieldDCFc1JcMFfIU ansible-k8s-server
EOF

chown -R deploy:deploy /home/deploy/.ssh

cat << EOF > /etc/sudoers.d/00-deploy
deploy ALL=(ALL) NOPASSWD: ALL
EOF
```
