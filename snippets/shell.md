# Shell

```sh
# convert Ansible tags into selectable list
ansible-playbook playbook.yml --list-tags \
  | sed -rn 's/^\s+TASK\sTAGS:\s\[(.*)\]$/\1/p' \
  | sed 's/, /\n/g' \
  | fzf --multi --ansi -i -1 --height=50% --reverse -0 --border \
  | xargs \
  | tr ' ' ','
```

---

```sh
# parse OS information
sed -rn 's/^ID=([a-z]+)/\1/p' /etc/os-release
```

---

```sh
# remove all the IUS php packages and replace them with remi php packages
yum list installed php72u* \
  | sed -rn 's/^(php72u-.*)\.(x86_64|noarch).*/\1/p' > /tmp/ius-php-packages
yum remove -y $(cat /tmp/ius-php-packages)
yum install -y $(cat /tmp/ius-php-packages | sed 's/php72u/php/g')
```
