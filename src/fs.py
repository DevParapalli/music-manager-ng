import base64
import os
from pathlib import Path

from filetype import guess
from mutagen import mp3, mp4

def get_directory(dir: str, ext: list=['mp3', 'wav', 'flac', 'm4a', 'aac', 'ogg']) -> tuple[list, list]:
    # https://stackoverflow.com/a/59803793
    subfolders, files = [], []

    for f in os.scandir(dir):
        if f.is_dir():
            subfolders.append(f.path)
        if f.is_file():
            if os.path.splitext(f.name)[1].lower().replace('.', "") in ext:  # NOSONAR
                files.append(f.path)

    for dir in list(subfolders):
        sf, f = get_directory(dir, ext)
        subfolders.extend(sf)
        files.extend(f)

    return subfolders, files

def get_image_key(keys):
    if 'APIC:Cover' in keys:
        return 'APIC:Cover'
    for key in keys:
        if key.startswith('APIC:'):
            return key


def get_song_metadata(file: str):
    """Returns metadata if supported by mutagen, else throws error."""
    if os.path.splitext(file)[1].lower() == ".mp3":
        audio = mp3.MP3(file)
        image_tag = get_image_key(audio.tags.keys())
        if image_tag:
            album_art = f"{audio[image_tag].mime}<!>{base64.b64encode(audio[image_tag].data).decode()}"
        else:
            album_art = f"/defaults/default_song_image.svg"
        # Read the standards for MP3 ID3 Tags and explanation for below.
        return {
            "content": "fs.file.metadata.mp3",
            "data": {
                "album_art": album_art,
                "title": ", ".join(audio["TIT2"].text),
                "album": ", ".join(audio["TALB"].text),
                "artist": ", ".join(audio["TPE1"].text),
                "duration": audio.info.length,
                "bitrate": audio.info.bitrate,
            }
        }
    if os.path.splitext(file)[1].lower() == ".m4a":
        audio = mp4.MP4(file)
        album_art_bytes = bytes(audio['covr'][0])
        mime = guess(album_art_bytes).mime
        return {
            "content": "fs.file.metadata.m4a",
            "data": {
                "album_art": f"{mime}<!>{base64.b64encode(album_art_bytes).decode()}",
                "title": ", ".join(audio["\xa9nam"]),
                "album": ", ".join(audio["\xa9alb"]),
                "artist": ", ".join(audio["\xa9ART"]),
                "duration": audio.info.length,
                "bitrate": audio.info.bitrate,
            }
        }


