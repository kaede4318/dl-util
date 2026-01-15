from subprocess import Popen, PIPE
from pathlib import Path

import os

CWD = os.getcwd()

# prepares video download command
def prepare_download_video_from_batch_file(input, output):
    cmd = [
        "yt-dlp",
        "-S", "vcodec:h264,res,acodec:m4a", # -S does NOT filter, only sort. will not fail if not found
        "-a", input, # input of links (txt file)
        "-P", output, # output location
        "--sleep-interval", "5", # sleep needed to avoid IP bans
        "--max-sleep-interval", "10", 
        "--embed-thumbnail",
        "--embed-metadata",
    ]
    return cmd

# download single video or from playlist
def prepare_download_video(input, output):
    cmd = [
        "yt-dlp",
        "-S", "vcodec:h264,res,acodec:m4a", # -S does NOT filter, only sort. will not fail if not found
        "-P", output, # output location
        "--sleep-interval", "5", # sleep needed to avoid IP bans
        "--max-sleep-interval", "10", 
        "--embed-thumbnail",
        "--embed-metadata",
        input
    ]
    return cmd

# note: don't know if track number metadata is working
def prepare_download_audio(input, output):
    cmd = [
        "yt-dlp",
        "-x", 
        "-P", output, # output location
        "--audio-format", "flac",
        "--sleep-interval", "5", # sleep needed to avoid IP bans
        "--max-sleep-interval", "10",
        "--parse-metadata", "playlist_index:%(track_number)s",
        "--embed-metadata",
        "-o", "%(playlist)s/%(title)s", # specify filename/location on top of -P option
        input
    ]
    return cmd

# runs yt-dlp command
def run(command):
    # stdout=PIPE ~ prints each line as it comes
    p = Popen(
        command, 
        stdout=PIPE, 
        stderr=PIPE,
        text=True,
        bufsize=1  # Line-buffered
    )

    for line in p.stdout:
        print(line.strip())

    p.wait()  # Wait for process to complete

    # proc.terminate()  # politely stop it
    # proc.kill()       # forcefully stop it

if __name__ == "__main__":
    INPUT_FILE = "./input/yt_links.txt"

    my_file = Path(INPUT_FILE)
    if not my_file.is_file():
        raise FileNotFoundError(str(my_file) + " doesn't exist")
    
    out = "./output/"
    # run(prepare_download_video(INPUT_FILE, out))
    # pl_link = "https://www.youtube.com/playlist?list=PL7h7m34DLvE9dR6FfttZZM2hNSUelfyr2"
    # pl_link = "https://youtube.com/playlist?list=PL7h7m34DLvE_jY0O0mYDWaFBaLmy3wurJ"
    # run(prepare_download_video(pl_link, out))
    run(prepare_download_audio("https://www.youtube.com/playlist?list=PL8sbCrEMTyLlLo3ehFJaLLpJ26FaGsi3O", out))