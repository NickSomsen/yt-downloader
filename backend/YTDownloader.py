from pytube import YouTube
from PIL import Image
import requests
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import math


def on_progress(stream, chunk, bytes_remaining):
    print(f"Progress: {round(100 - (bytes_remaining / stream.filesize * 100), 1)}%")


def on_complete(stream, file_path):
    print(f"Download completed: {file_path}")


def get_thumbnail_stream(video):
    # the parameters in the url result in a cropped image, so remove them.
    # More info on thumbnail qualities:
    # https://stackoverflow.com/questions/2068344/how-do-i-get-a-youtube-video-thumbnail-from-the-youtube-api
    img_url = video.thumbnail_url.split("?")[0]
    return requests.get(img_url, stream=True)


def convert_size(size_bytes):
    if size_bytes == 0:
        return "0B"

    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return f"{s}{size_name[i]}"


def show_thumbnail(response):
    img = Image.open(response.raw)

    plt.figure()
    plt.imshow(img)
    plt.xticks([])
    plt.yticks([])
    plt.grid(False)
    plt.show()
    plt.close()


video = YouTube("https://www.youtube.com/watch?v=cLArh72FEYQ",
                on_progress_callback=on_progress,
                on_complete_callback=on_complete)
img_stream = get_thumbnail_stream(video)
show_thumbnail(img_stream)

video.streams.filter(only_video=True, subtype="mp4").order_by("resolution").last().download()

print(convert_size(video.streams.get_highest_resolution().filesize))

# YouTube offers streams that contain both video and audio (progressive) and
# streams that contain only video or audio (DASH). The highest quality streams
# are DASH streams, but this comes with the implication that the video and
# audio tracks need to be merged (e.g. with FFmpeg). Progressive streams have
# a maximum quality of 720p.

# Get the highest progressive stream (video + audio):
# video.streams.get_highest_resolution()

# Get the highest video-only stream
# video.streams.filter(only_video=True, subtype="mp4").order_by("resolution").last().download()
# NOTE: .get_video_only() unfortunately doesn't exist. Also don't use asc()
# and desc() because they don't order based on an attribute. Instead, filter
# for video-only mp4 streams, and order them by resolution (grab last stream
# ordering is done ascending).
# NOTE: sometimes mp4 doesn't work while webm does for Windows video player.
# VLC Media Player can open everything though.

# Get the highest audio-only stream:
# video.streams.get_audio_only(subtype="mp4").download()
# NOTE: this returns the highest bitrate ("abr" attribute) audio stream.
# subtype=webm is also an option and can offer higher quality, but webm is not
# as widely supported as mp4.
