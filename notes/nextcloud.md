# Nextcloud

```sh
# scan entire directory for new files
docker exec \
    --user www-data \
    nextcloud php occ files:scan --all

# scan specific directory for new files
docker exec nextcloud php occ files:scan \
    --user www-data \
    --path="path/to/dir"
```