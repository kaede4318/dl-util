from subprocess import Popen, PIPE
from pathlib import Path
from shellwords import ShellWords
import os

CWD = os.getcwd()
s = ShellWords()

env = os.environ.copy()
env["PATH"] = "/opt/homebrew/bin:" + env["PATH"]  # adjust if necessary

# runs yt-dlp command
def run(link=None, output_location="./output/"):
    command = f'yt-dlp -P {output_location} -f "bv[vcodec^=avc1][ext=mp4]+ba[acodec^=mp4a][ext=m4a]/mp4" {link}'
    command += ' --user-agent "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"'
    tokens = s.parse(command) # needed to remove quotes as shell does

    # stdout=PIPE ~ prints each line as it comes
    p = Popen(tokens, stdout=PIPE, stderr=PIPE, text=True, bufsize=1, env=env)

    # Read both stdout and stderr line by line
    for line in p.stdout:
        print("STDOUT:", line.strip())
    for line in p.stderr:
        print("STDERR:", line.strip())

    p.wait()
    print("Process exited with code", p.returncode)

    # proc.terminate()  # politely stop it
    # proc.kill()       # forcefully stop it

if __name__ == "__main__":
    # testing
    INPUT = "https://www.youtube.com/watch?v=cTDK5Bluh5A" 
    out = "./output/"
    run(link=INPUT, output_location=out)
