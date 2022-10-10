# HandBrake

```sh
sudo docker pull ntodd/video-transcoding
sudo docker run -itv "`pwd`":/data ntodd/video-transcoding
transcode-video --scan ./
# transcode feature title to h265 mkv
transcode-video --encoder x265 -o movie.mkv ./
# transcode a specific title to h265 mkv
transcode-video --encoder x265 --title <title> -o title.mkv ./
```