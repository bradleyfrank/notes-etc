#!/usr/bin/env python3

import argparse
import json
import re
import shutil
from pathlib import PosixPath

import logzero
import requests

# from mutagen import FileType, MutagenError
from mutagen.flac import FLAC, FLACNoHeaderError
from mutagen.mp3 import MP3, ID3FileType, HeaderNotFoundError
from pydub import AudioSegment
from pydub.exceptions import CouldntDecodeError, CouldntEncodeError


DEFAULT_SOURCE_DIR = PosixPath.cwd()
DEFAULT_OUTPUT_DIR = PosixPath.home() / "Music" / "mp3z"


def parse_args() -> argparse.ArgumentParser:
    args = argparse.ArgumentParser(prog="mp3z")
    args_stdout = args.add_mutually_exclusive_group()
    args_stdout.add_argument("-v", "--verbose", help="verbose output", action="store_true")
    args_stdout.add_argument("-d", "--debug", help="enable debugging", action="store_true")
    args_stdout.add_argument("-q", "--quiet", help="disable all ouput", action="store_true")

    subparsers = args.add_subparsers(help="Subcommands", dest="subcommand")

    args_convert = subparsers.add_parser("convert", help="Convert FLAC to MP3")
    args_convert.add_argument(
        "-s",
        "--source",
        help="source directory",
        type=PosixPath,
        default=DEFAULT_SOURCE_DIR,
    )
    args_convert.add_argument(
        "-o",
        "--output",
        help="output directory",
        type=PosixPath,
        default=DEFAULT_OUTPUT_DIR,
    )

    args_tag = subparsers.add_parser("tag", help="tag MP3s via MusicBrainz")
    args_tag.add_argument("-s", "--source", help="source directory", type=PosixPath)

    args_rename = subparsers.add_parser("rename", help="Rename MP3 based on ID3 tags")
    args_rename.add_argument(
        "-s",
        "--source",
        help="source directory",
        type=PosixPath,
        default=DEFAULT_SOURCE_DIR,
    )
    args_rename.add_argument(
        "-o",
        "--output",
        help="output directory",
        type=PosixPath,
        default=DEFAULT_OUTPUT_DIR,
    )

    return args.parse_args()


def set_logging(debug: bool, quiet: bool, verbose: bool) -> logzero.logging.Logger:
    if debug:
        level = 10
        log_format = "%(color)s[%(asctime)s] %(message)s%(end_color)s"
    elif verbose:
        level = 10
        log_format = "%(color)s%(message)s%(end_color)s"
    elif quiet:
        level = 40
        log_format = "%(color)s[%(levelname)1.1s] %(message)s%(end_color)s"
    else:
        level = 20
        log_format = " %(color)s%(message)s%(end_color)s"

    formatter = logzero.LogFormatter(fmt=log_format)
    return logzero.setup_default_logger(level=level, formatter=formatter)


class Song:
    def __init__(self, logger: logzero.logging.Logger, source: PosixPath, output_dir: PosixPath):
        self.lz = logger
        self.source = source
        self.output = output_dir / self.source.with_suffix(".mp3").name
        self.album, self.title, self.disc, self.track = ["", "", "", ""]
        self.track_number, self.total_tracks, self.disc_number, self.total_discs = [0, 0, 0, 0]

        try:
            FLAC(self.source)
        except FLACNoHeaderError:
            self.is_flac = False
        else:
            self.is_flac = True
            self.convert_to_mp3()

        try:
            MP3(self.source)
        except HeaderNotFoundError:
            self.is_mp3 = False
        else:
            self.is_mp3 = True
            shutil.copy(self.source, self.output)

        self.is_audio = self.is_flac or self.is_mp3

    def convert_to_mp3(self) -> None:
        self.lz.info(f"\U0000f001  '{self.source.name}' \U000027a1 '{self.output.name}'")

        try:
            flac = AudioSegment.from_file(self.source, format="flac")
        except CouldntDecodeError as exc:
            self.lz.error(f"Error: could not decode '{self.source.name}'")
            raise IOError from exc

        try:
            conversion_result = flac.export(self.output, format="mp3", bitrate="320k")
        except (CouldntEncodeError, AttributeError) as exc:
            self.lz.error(f"Error: could not encode '{self.source.name}'")
            raise IOError from exc

        if not conversion_result:
            self.lz.error(f"Error: could not convert '{self.source.name}'")
            raise IOError

    def sanitize(self, s):
        # TODO: Make this more robust, e.g. allow Japanese characters
        return "".join([c if c.isalnum() else "_" for c in s])

    def parse_id3_tags(self, file: PosixPath, song: ID3FileType) -> dict:
        self.lz.info(f"  \U0001f50e {file.relative_to(self.source)}")

        tags_present = [tag in song for tag in ["TALB", "TIT2", "TRCK", "TPOS"]]

        if not tags_present:
            e = f"Error: '{self.source.name}' is missing required ID3 tags"
            self.lz.error(f"     {e}")
            raise KeyError(e)

        self.album = song.get("TALB", "")[0]
        self.title = song.get("TIT2", "")[0]
        self.track_number, self.total_tracks = song.get("TRCK", "/")[0].split("/")
        self.disc_number, self.total_discs = song.get("TPOS", "/")[0].split("/")
        self.track = self.track_number.zfill(len(self.total_tracks))
        self.disc = self.disc_number.zfill(len(self.total_discs))


class Album:
    def __init__(self, logger, source_dir, output_dir):
        self.lz = logger
        self.source_dir = source_dir
        self.output_dir = output_dir
        self.files = self.walk(self.source_dir)
        self.songs = []

        uuid_regex = re.compile("[0-9a-fA-F]{8}-([0-9a-fA-F]{4}-){3}[0-9a-fA-F]{12}")

        for file in self.files:
            if uuid_regex.match(file.name):
                self.mbid = file.name
                continue
            song = Song(self.lz, file, self.output_dir)
            if song.is_audio:
                self.songs.append(song)
        # self.mp3s = [song.convert_to_mp3() if song.is_flac else song for song in self.songs]
        # self.songs = [song for song := Song(file) in self.files if song.is_filetype(file, FLAC)]
        # self.mp3s = [mp3 for song in self.songs if (mp3 := self.flac_to_mp3(song))]

    def walk(self, directory: PosixPath) -> list:
        self.lz.debug(f"\U0000f4d3  {directory.relative_to(self.source_dir)}")
        files = []
        for child in directory.iterdir():
            if child.is_file():
                files.append(child)
                self.lz.debug(f"\U0000f0c6  {child.relative_to(directory)}")
            elif child.is_dir():
                files.extend(self.walk(child))
            else:
                self.lz.debug(f"\U0000f0c6  {child.name} not a file or directory")
        return files


#    def tag(self) -> None:
#        for mp3 in self.songs:
#            self.lz.debug(f"Getting album ID: {self.mbid}")
#
#            metadata = mbz.get_release_by_id(album_id, includes=["media", "recordings"])
#            metadata = {}
#            dictionary = json.load(metadata)
#            files_in_album = [file for file in files if album.name in file.parts]
#            mp3s = [song for song in files_in_album if self.is_filetype(song, ID3)]
#            self.lz.debug(mp3s)

#    def rename(self, files: list) -> None:
#        metadata = [
#            self.parse_id3_tags(file, mp3) for file in files if (mp3 := self.is_filetype(file, MP3))
#        ]
#
#        for m in metadata:
#            directory = self.output_dir / m["album"]
#            filename = f"{m['disc']}x{m['track']}.{m['title']}{m['extension']}"
#
#            self.lz.info(f"\U0001F4CB {filename}")
#            shutil.copy(m["file"], directory / filename)


flags = parse_args()
LZ = set_logging(flags.debug, flags.quiet, flags.verbose)
flags.output.mkdir(parents=True, exist_ok=True)

# if not flags.one:
#    for folder in flags.source.iterdir():
#        files = walk(flags.source, flags.source)
#
# if not files:
#    LZ.warning(f"No files found")
#    sys.exit(0)

# match flags.subcommand:
#    case "convert":
#        convert(files, flags)
#    case "rename":
#        rename(files, flags)
#    case "tag":
#        tag(files, flags)
