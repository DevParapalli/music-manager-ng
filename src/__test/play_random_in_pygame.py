import pygame
import pydub
import io
import time
from mutagen.id3 import ID3

with open(r"C:\DevParapalli\Projects\musimanager_test\mkfIc0arbCY.mp3", "rb") as file:
    
    import logging

    l = logging.getLogger("pydub.converter")
    l.setLevel(logging.DEBUG)
    l.addHandler(logging.StreamHandler())
    # Use this when frozen
    #pydub.AudioSegment.converter = r"C:\DevParapalli\Projects\music-manager-ng\vendor_bin\ffmpeg.exe"
    pygame.mixer.init()
    tags = ID3(file)
    print(tags.keys())
    # use a function here to get the actual data depending on the file type
    audio = pydub.AudioSegment.from_file(file)
    filelike = io.BytesIO()
    filelike = audio.export(filelike, format="flac")
    filelike.seek(0)
    pygame.mixer.music.load(filelike, namehint="flac")
    pygame.mixer.music.play()
    pygame.mixer.music.set_pos(30)
    time.sleep(45) 
    pygame.mixer.music.stop()
    time.sleep(5)
