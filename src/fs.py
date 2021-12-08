import os

def get_recursive_directory(dir: str, ext: list):
    # https://stackoverflow.com/a/59803793
    subfolders, files = [], []

    for f in os.scandir(dir):
        if f.is_dir():
            subfolders.append(f.path)
        if f.is_file():
            if os.path.splitext(f.name)[1].lower().replace('.', "") in ext:  # NOSONAR
                files.append(f.path)

    for dir in list(subfolders):
        sf, f = get_recursive_directory(dir, ext)
        subfolders.extend(sf)
        files.extend(f)
    return subfolders, files