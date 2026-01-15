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

def prepare_download_audio_from_batch_file(input, output):
    cmd = [
        "yt-dlp",
        "-x",
        "-a", input, # input of links (txt file)
        "-P", output, # output location
        "--audio-format", "flac",
        "--sleep-interval", "5", # sleep needed to avoid IP bans
        "--max-sleep-interval", "10",
        "--parse-metadata", "playlist_index:%(track_number)s",
        "--embed-metadata",
        "-o", "%(playlist)s/%(title)s", # specify filename/location on top of -P option
    ]
    return cmd

# runs yt-dlp command
def run(link=None, batch_file=None, output_location="./output/", audio_only=False):
    # validate inputs
    if (link is None and batch_file is None) or (link and batch_file):
        raise ValueError("You must provide exactly one of 'link' or 'batch_file'.")
    
    input_path, output_path = Path(batch_file), Path(output_location)
    if not input_path.is_file():
        raise FileNotFoundError(str(input_path) + " doesn't exist")
    elif not output_path.is_dir():
        raise FileNotFoundError(str(output_path) + " doesn't exist")
    
    command = []
    if link:
        if audio_only:
            command = prepare_download_audio(link, output_location)
        else:
            command = prepare_download_video(link, output_location)
    elif batch_file:
        if audio_only:
            command = prepare_download_audio_from_batch_file(batch_file, output_location)
        else:
            command = prepare_download_video_from_batch_file(batch_file, output_location)
    else:
        raise ValueError("Something went wrong")

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
    INPUT_FILE = "./input/audio_only.txt"
    out = "./output/"
    run(batch_file=INPUT_FILE, output_location=out, audio_only=True)