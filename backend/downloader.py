from subprocess import Popen, PIPE
from pathlib import Path

import os

CWD = os.getcwd()

# runs yt-dlp command
def run(link=None, output_location="./output/"):
    command = f'yt-dlp -P {output_location} -f "bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4" {link}'
    command = command.split(" ")

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
    INPUT = "https://www.youtube.com/watch?v=cTDK5Bluh5A" 
    out = "./output/"
    run(link=INPUT, output_location=out, audio_only=False)
