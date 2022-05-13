# Apps

## MusicBrainz

```none
%%$if($lt(%discnumber%,10),0)%discnumber%x$if($lt(%tracknumber%,10),0)%tracknumber%-$replace(%title%, ,_)%%
```

## HandBrake

```sh
sudo docker pull ntodd/video-transcoding
sudo docker run -itv "`pwd`":/data ntodd/video-transcoding
transcode-video --scan ./
# transcode feature title to h265 mkv
transcode-video --encoder x265 -o movie.mkv ./
# transcode a specific title to h265 mkv
transcode-video --encoder x265 --title <title> -o title.mkv ./
```

## Nextcloud

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

## Plex

```sh
# get list of albums
./Plex\ Media\ Scanner -t -c 6 \
  | grep 'Poster' -A 1 \
  | grep -E '\[[0-9]{4}\]' \
  | sed 's/\s*\*\s//'
```
