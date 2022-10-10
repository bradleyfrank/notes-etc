# Synology

Installing tmux & other CLI tools:

1. Add [SynoCommunity](https://synocommunity.com)
2. Install CLI Tools package
3. Install Python3 package
4. Install Pip

```sh
# fix clock for 2FA
synoservicecfg --pause ntpd-client
ntpdate north-america.pool.ntp.org
synoservicecfg --restart ntpd-client
```
