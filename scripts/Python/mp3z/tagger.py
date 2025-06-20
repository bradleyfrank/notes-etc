#!/usr/bin/env python3

import musicbrainzngs as mbz

mbz.set_useragent('mp3z.franklybrad.com', '0.1')

def get_album_from_id(album_id, logger):
    logger.debug(f"Getting album ID: {album_id}")
    metadata = mbz.get_release_by_id(album_id, includes=["media","recordings"])
    dictionary = json.load(metadata)
    return metadata
    #album = {}
    #total_tracks = 0
    #for disc in metadata["release"]["medium-list"]:
    #    total_tracks += disc["track-count"]
    #    for track in disc["track-list"]:
    #        tracks[track["number"]] = track["recording"]["title"]

    #album[album_id] = {
    #    "title": release["title"],
    #    "total_discs": metadata["medium-count"],
    #    "total_tracks": total_tracks,
    #    "tracks": tracks
    #}
