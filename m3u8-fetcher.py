import os
import subprocess
import sys
import tempfile
from urllib.parse import urlparse

m3u8_url = sys.argv[1]
output = sys.argv[2]

m3u8_parsed = urlparse(m3u8_url)
base_url = m3u8_url.strip(os.path.basename(m3u8_parsed.path))

with tempfile.TemporaryDirectory() as tmpdirname:
    print('created temporary directory', tmpdirname)

    try:
        retcode = subprocess.call("wget " + m3u8_url + " -O " + tmpdirname + "/" + "playlist.m3u8", shell=True)
        print("wget of m3u8 returned", retcode, file=sys.stderr)
    except OSError as e:
        print("Execution failed:", e, file=sys.stderr)

    f_mp4_playlist = open(tmpdirname + "/" + "mp4_playlist.txt", "w")
    for ts_name in open(tmpdirname + "/" + "playlist.m3u8", 'r'):
        ts_name = ts_name.strip("\n")
        if ts_name[:1] != '#':
            print("Downloading: " + ts_name)
            try:
                print("wget " + base_url + ts_name + " -O " + tmpdirname + "/" + ts_name)
                retcode = subprocess.call("wget " + base_url + ts_name + " -O " + tmpdirname + "/" + ts_name,
                                          shell=True)
                print("wget of " + ts_name + " returned", retcode, file=sys.stderr)
                f_mp4_playlist.write("file " + tmpdirname + "/" + ts_name + "\n")
                f_mp4_playlist.flush()
                print("Saved as: " + tmpdirname + "/" + ts_name)
            except OSError as e:
                print("Execution failed:", e, file=sys.stderr)

    f_mp4_playlist.close()
    try:
        retcode = subprocess.call(
            "ffmpeg -f concat -safe 0 -i " + tmpdirname + "/" + "mp4_playlist.txt" + " -c copy ./" + output, shell=True)
        print("ffmpeg " + " returned", retcode, file=sys.stderr)
    except OSError as e:
        print("Execution failed:", e, file=sys.stderr)
