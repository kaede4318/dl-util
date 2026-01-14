# youtube examples
these examples are verified to work with yt. other platforms need further testing

important note: double quotes are often needed for the commands. do not leave them out!

## downloading videos from a batch .txt file:
```
yt-dlp -S vcodec:h264,res,acodec:m4a -a "<INPUT_.txt_FILE>" -P "<OUTPUT DIR>" --sleep-interval 5 --max-sleep-interval 10 --embed-thumbnail --embed-metadata"
```

## downloading audio only from a playlist:
```
yt-dlp -x -o "%(playlist)s/%(playlist_index)s - %(title)s.%(ext)s" -P <OUTPUT DIR>" --audio-format "<FORMAT>" --sleep-interval 5 --max-sleep-interval 10 --embed-metadata "<PLAYLIST_NAME>"
```
formats not originally from site are supported through post-processing using ffmpeg