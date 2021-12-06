# NOTES for Developers

## Building the final bundle

The final bundle needs to contain the correct arch and bitness of the target system, initially a Win64 bundle will be created while including the ffmpeg and libav as data deps,

- a function will be used to get a path for ffmpeg, ffplay, libav and avplay. The function should return the system path incase the application is not frozen (bundled) or the sys._MEIPASS if the application is frozen
- Bundle is shared as a compressed .zip file. Extract to whatever folder and run. The .zip will be named with the target system, arch, bitness and the version. Preferably `app-windows-amd64-64-1.0.0.zip` or something similar.
- Creating a simple build.py script that will be used to build the final bundle
