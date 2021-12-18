from mutagen import (
    aac,
    apev2,
    aiff,
    asf,
    dsdiff,
    id3,
    mp4,
    flac,
    musepack,
    ogg,
    oggvorbis,
    oggopus,
    smf,
    wave,
    wavpack
)
import typing
from base64 import b64encode


def tags_mp3(filelike: typing.BinaryIO) -> dict[str, str]:
    if filelike.seekable():
        filelike.seek(0)
    audio = id3.ID3(filelike)
    artist = audio.get('TPE1', "Unknown").__str__()
    album = audio.get('TALB',  "Unknown").__str__()
    title = audio.get('TIT2', "Unknown").__str__()
    _image_tag = ""
    for tag in audio.keys():
        if tag.startswith("APIC:"):
            _image_tag = tag

    image_bytes = b64encode(audio.get(_image_tag).data)

    return {
        "artist": artist,
        "album": album,
        "title": title,
        "image": image_bytes.decode("utf-8")
    }


def tags_mp4(filelike: typing.BinaryIO) -> dict[str, str]:
    if filelike.seekable():
        filelike.seek(0)
    audio = mp4.MP4(filelike)
    artist = audio.get('\xa9ART', "Unknown").__str__()
    album = audio.get('\xa9alb',  "Unknown").__str__()
    title = audio.get('\xa9nam', "Unknown").__str__()
    if 'covr' in audio.keys():
        image_bytes = b64encode(audio.get('covr'))
    else:
        image_bytes = b""
    #image_bytes = b64encode(audio.get(_image_tag).data)

    return {
        "artist": artist,
        "album": album,
        "title": title,
        "image": image_bytes.decode("utf-8")
    }


