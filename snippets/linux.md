# Linux

```sh
# remove all the IUS php packages and replace them with remi php packages
yum list installed php72u* \
  | sed -rn 's/^(php72u-.*)\.(x86_64|noarch).*/\1/p' > /tmp/ius-php-packages
yum remove -y $(cat /tmp/ius-php-packages)
yum install -y $(cat /tmp/ius-php-packages | sed 's/php72u/php/g')
```