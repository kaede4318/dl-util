import shlex
from cli_to_api import cli_to_api
import yt_dlp

yt_cli_string = "yt-dlp -S vcodec:h264,res,acodec:m4a -a \"./input/yt_test.txt\" -P \"./output/\" --sleep-interval 5 --max-sleep-interval 10 --embed-thumbnail --embed-metadata"
audio_only_playlist = "yt-dlp -x -o \"%(playlist)s/%(playlist_index)s - %(title)s.%(ext)s\" -P \"./output/\" --audio-format \"flac\" --sleep-interval 5 --max-sleep-interval 10 --embed-metadata \"<PLAYLIST_NAME>\""

yt_batch_dl = {
    'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]',
    'merge_output_format': 'mp4',
    'outtmpl': {
        'pl_thumbnail': '',
    },
    'paths': {
        'home': './output/',
    },
    'writethumbnail': True,
    'postprocessors': [
        {
            'key': 'FFmpegMetadata',
            'add_chapters': True,
            'add_metadata': True,
            'add_infojson': 'if_exists',
        },
        {
            'key': 'EmbedThumbnail',
            'already_have_thumbnail': False,
        },
    ],
    'sleep_interval': 5.0,
    'max_sleep_interval': 10.0,
}

yt_playlist_dl_audio_only = {
    'format': 'bestaudio/best', 
    'outtmpl': {
        'default': '%(playlist)s/%(playlist_index)s - %(title)s.%(ext)s'
    }, 
    'paths': {
        'home': './output/'
    }, 
    'final_ext': 'flac', 
    'postprocessors': [
        {
            'key': 'FFmpegExtractAudio', 
            'preferredcodec': 'flac', 
            'preferredquality': '5', 
            'nopostoverwrites': False
        }, 
        {
            'key': 'FFmpegMetadata', 
            'add_chapters': True, 
            'add_metadata': True, 
            'add_infojson': 'if_exists'
        }
    ], 
    'sleep_interval': 5.0, 
    'max_sleep_interval': 10.0
}

def convert_cli_to_api(cli_string):
    # Convert string to list safely
    cli_args = shlex.split(cli_string)

    opts = cli_to_api(cli_args)
    return opts

def process_inputs(line):
    res = line.strip() # remove whitespace

    # it seems like each site adds tracking identifiers when you use the "share" or "copy link" feature
    res = res.split("?utm_source=", 1)[0] # remove tracking from instagram links
    return res.split("?si=", 1)[0] # remove tracking from yt links

def main():
    INPUT_URL = './input/yt_links.txt'
    URLS = []
    with open(INPUT_URL) as f:
        # this would be more efficient in the future, if f is big.
        for line in f:
            clean_line = process_inputs(line)
            URLS.append(clean_line)
            # process(line)

    inputs = URLS
    with yt_dlp.YoutubeDL(yt_batch_dl) as ydl:
        ydl.download(inputs)


if __name__ == "__main__":
    main()
