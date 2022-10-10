# Plex

```sh
# get list of albums
./Plex\ Media\ Scanner -t -c 6 \
  | grep 'Poster' -A 1 \
  | grep -E '\[[0-9]{4}\]' \
  | sed 's/\s*\*\s//'
```