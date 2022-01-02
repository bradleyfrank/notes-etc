# Containers

```sh
# authenticate to GitHub Docker Registry
cat ~/.github_token | docker login docker.pkg.github.com -u <username> --password-stdin
```

## Docker

```sh
# pruning
docker system prune [-a|--all]
docker rm $(docker ps -a -q)
docker image prune --all
```
