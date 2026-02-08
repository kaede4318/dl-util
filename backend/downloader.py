from subprocess import Popen, PIPE
from pathlib import Path
from shellwords import ShellWords
import tempfile
import os

CWD = os.getcwd()
s = ShellWords()

env = os.environ.copy()
env["PATH"] = "/opt/homebrew/bin:" + env["PATH"]  # adjust if necessary

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/118.0.0.0 Safari/537.36"
)

# runs yt-dlp command
def run(link: str) -> Path:
    # Create a unique temporary file for this download
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        tmp_path = tmp_file.name
        
    command = [
        "yt-dlp",
        "-o", "/tmp/dl/%(title)s - %(uploader)s [%(id)s].%(ext)s",
        "-f", "bv[vcodec^=avc1][ext=mp4]+ba[acodec^=mp4a][ext=m4a]/mp4",
        "--user-agent", USER_AGENT,
        "--restrict-filenames",
        "--sleep-interval", "5", # sleep needed to avoid IP bans
        "--max-sleep-interval", "10", 
        "--exec", f"echo {{}} > {tmp_path}", # parse this file to find filename
        link,
    ]
    # look if you are missing any commas ;)
    # btw, --restrict-filenames will get rid of non-ASCII characters like CJK characters
    # "--progress-template", "%(progress)j", # prints out progress as json (useful for parsing)

    p = Popen(
        command,
        stdout=PIPE,
        stderr=PIPE,
        text=True,
        bufsize=1,
        env=env,
    )

    # Read both stdout and stderr line by line
    for line in p.stdout:
        print("STDOUT:", line.strip())
    for line in p.stderr:
        print(line.strip())

    # Read the filename after download
    with open(tmp_path, "r") as f:
        final_filename = f.read().strip()
    
    os.unlink(tmp_path) # remove after queue full

    return Path(final_filename)


if __name__ == "__main__":
    # testing
    INPUT = "https://www.youtube.com/watch?v=cTDK5Bluh5A" 
    jeffbeck = "https://www.youtube.com/watch?v=WNNkbE6EU3w" 
    out = "./output/"
    run(link=jeffbeck)
