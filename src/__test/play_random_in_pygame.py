import pygame
import pydub
import io
import time
from phrydy import MediaFile
import logging
import typing
from base64 import b64encode
from pprint import pprint


def get_tags(media: typing.BinaryIO):
    if media.seekable():
        media.seek(0)
    tags = MediaFile(media)
    artist = getattr(tags, 'artist', 'Unknown')
    album = getattr(tags, 'album', 'Unknown')
    title = getattr(tags, 'title', 'Unknown')
    _image_bytes = getattr(tags, 'art', None)
    if media.seekable():
        media.seek(0)
    return {
        "artist": artist,
        "album": album,
        "title": title,
        # TODO: Modify this when dev is over
        "image": _image_bytes[:100]
    }

def _get_pygame_playable_flac(media: typing.BinaryIO):
    if media.seekable():
        media.seek(0)
    audio = pydub.AudioSegment.from_file(media)
    filelike = io.BytesIO()
    filelike = audio.export(filelike, format="flac")
    filelike.seek(0)
    if media.seekable():
        media.seek(0)
    return filelike


with open(r"C:\Users\parap\Music\1hKZqJwewHA.mp3", "rb") as file:
    l = logging.getLogger("pydub.converter")
    l.setLevel(logging.DEBUG)
    l.addHandler(logging.StreamHandler())
    # Use this when frozen
    #pydub.AudioSegment.converter = r"C:\DevParapalli\Projects\music-manager-ng\vendor_bin\ffmpeg.exe"
    pygame.mixer.init()

    pprint(get_tags(file))
    pygame.mixer.music.load(_get_pygame_playable_flac(file), namehint="flac")
    pygame.mixer.music.play()
    pygame.mixer.music.set_pos(30)
    pygame.mixer.music.set_volume(0.25)
    time.sleep(30)
    pygame.mixer.music.stop()
    # time.sleep(5)
