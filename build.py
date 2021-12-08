import subprocess
import pathlib
import requests
import zipfile
import tarfile
import hashlib
import shutil
import os

BASE_DIR = pathlib.Path(__file__).parent.resolve()
TEMP_DIR = BASE_DIR.joinpath('tmp')
VENDOR_BIN_DIR = BASE_DIR.joinpath('vendor_bin')

## VERIFICATION FUNCTIONS
def hash_bytestr_iter(bytesiter, hasher, ashexstr=True):
    for block in bytesiter:
        hasher.update(block)
    return hasher.hexdigest().lower() if ashexstr else hasher.digest()

def file_as_blockiter(afile, blocksize=65536):
    with afile:
        block = afile.read(blocksize)
        while len(block) > 0:
            yield block
            block = afile.read(blocksize)

class CorruptedDownloadError(Exception):
    pass

## Extract and setup ffmpeg and avconv
# Download FFmpeg
def download_extract_ffmpeg():
    remote_file_url = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-git-full.7z" # Hardcoded for now
    remote_file_hash = "9e8ad8fd908532035a93e0d3461df6b3b410815301dff1bd3224615cd546716e" # Hardcoded for now
    local_archive_file_path = TEMP_DIR.joinpath(remote_file_url.split('/')[-1])
    if not local_archive_file_path.exists(): 
        with requests.get(remote_file_url, stream=True) as r:
            current_size = 0
            with open(local_archive_file_path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192): 
                    if chunk:
                        current_size += len(chunk)
                        f.write(chunk)
                        print(f"[BUILD] Downloading FFMPEG: {current_size}/{r.headers['Content-Length']}")
    # Verify hash
    returned_hash = hash_bytestr_iter(file_as_blockiter(open(local_archive_file_path, 'rb')), hashlib.sha256())
    if returned_hash != remote_file_hash:
        raise CorruptedDownloadError("Hash mismatch for downloaded file")
        
    # Extract
    if local_archive_file_path.suffix == '.7z':
        subprocess.call(['7z.exe', 'x', local_archive_file_path, '-o' + str(TEMP_DIR/'ffmpeg'), '-aos'])
    elif local_archive_file_path.suffix == '.zip':
        with zipfile.ZipFile(local_archive_file_path) as archive:
            archive.extractall(TEMP_DIR / 'ffmpeg')
    elif local_archive_file_path.suffix == '.tar.gz':
        with tarfile.open(local_archive_file_path) as archive:
            archive.extractall(TEMP_DIR / 'ffmpeg')
    # At this point ffmpeg has been extracted to TEMP_DIR/ffmpeg
    # Move ffmpeg to vendor_bin
    ffmpeg_path = os.listdir(TEMP_DIR / 'ffmpeg')[0]
    shutil.copytree(TEMP_DIR / 'ffmpeg' / f'{ffmpeg_path}' /'bin', str(VENDOR_BIN_DIR) + os.path.sep, dirs_exist_ok=True)


if __name__ == "__main__":
    download_extract_ffmpeg()
    #print("NOT COMPLETED")
