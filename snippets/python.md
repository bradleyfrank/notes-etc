# Python

```python
class myLogger:

    def __init__(self, debug_enabled=False):
        self.logger = logging.getLogger('mylogger')

        log_level = 10 if debug_enabled else 0
        log_format = logging.Formatter('[%(asctime)s] [%(levelname)8s] %(message)s', '%H:%M:%S')

        self.logger.setLevel(log_level)

        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(log_format)
        console_handler.setLevel(log_level)
        self.logger.addHandler(console_handler)

    def log(self, lvl, msg):
        level = logging.getLevelName(lvl.upper())
        self.logger.log(level, msg)
```

```python
# parsing kubeconfig
with open(Path.home() / ".kube/config", "r") as f:
    kubeconfig = yaml.safe_load(f)
clusters = [cluster["name"].split("_")[3] for cluster in kubeconfig["clusters"]]
```

```python
# iterate over mutagen mimetype and get extension
[e for m in song.mime if (e := mimetypes.guess_extension(m)) is not None][0]
```

```python
KEY_SEARCH = {
    "tracknumber": ["number", "track"],
    "discnumber": ["number", "disc"],
    "totaltracks": ["total","track"],
    "totaldiscs": ["total","disc"],
    "album": ["album"],
    "title": ["title"]
}

def flac_tag_search(keys: list) -> dict:
    tag_keys = {}
    for tag, substrings in KEY_SEARCH.items():
        regex = "".join([f"(?=.*{s})" for s in substrings])
        key = [k for k in keys if re.search(f"^{regex}.*$", k, re.IGNORECASE)]
        if not key:
            print(f"  \U0001f6D1 {Fore.RED}`{tag}` not found!")
            sys.exit(1)
        tag_keys[tag] = key[0]
    return tag_keys


def parse_id3_tags(file: PosixPath) -> dict:
    printm(f"  \U0001f50e {Fore.CYAN}{file.name}")

    def get_flac_tags(song):
        tags = {}
        for tag, key in flac_tag_search(song.keys()).items():
            tags[tag] = song[key]
        return tags

    match file.suffix:
        case ".flac":
            song = FLAC(file)
            tags = get_flac_tags(song)
            album = tags["album"][0]
            title = tags["title"][0]
            tracknumber = tags["tracknumber"][0]
            totaltracks = tags["totaltracks"][0]
            discnumber = tags["discnumber"][0]
            totaldiscs = tags["totaldiscs"][0]
        case ".mp3":
            song = ID3(file)
            album = song["TALB"][0]
            title = song["TIT2"][0]
            tracknumber, totaltracks = song["TRCK"][0].split("/")
            discnumber, totaldiscs = song["TPOS"][0].split("/")
        case _:
            return {}

    return {
        "file": file,
        "album": sanitize(album),
        "title": sanitize(title),
        "track": tracknumber.zfill(len(totaltracks)),
        "disc": discnumber.zfill(len(totaldiscs)),
        "extension": file.suffix,
    }
```