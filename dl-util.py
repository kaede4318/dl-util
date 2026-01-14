from subprocess import Popen, PIPE
import os

CWD = os.getcwd()

# YOUTUBE DOWNLOADING
INPUT_FILE = "./input/yt_test.txt"
cmd = [
    "yt-dlp",
    "-S", "vcodec:h264,res,acodec:m4a", # -S does NOT filter, only sort. will not fail if not found
    "-a", INPUT_FILE,
    "-P", "./output/",
    "--sleep-interval", "5", # sleep needed to avoid IP bans
    "--max-sleep-interval", "10", 
    "--embed-thumbnail",
]

# stdout=PIPE ~ prints each line as it comes
p = Popen(
    cmd, 
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