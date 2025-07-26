from pytubefix import YouTube
import math


class Video:

    def __init__(self, url):
        self._yt = YouTube(url)
        self.id = self._yt.video_id
        self.json = {
            "video_id": self._yt.video_id,
            "title": self._yt.title,
            # the params in the url result in a cropped image so remove them
            "thumbnail_url": self._yt.thumbnail_url.split("?")[0],
            "author": self._yt.author,
            "length": self.convert_length(self._yt.length),
            "tracks": {
                "progressive": self.get_tracks(progressive=True),
                "only_video": self.get_tracks(only_video=True),
                "only_audio": self.get_tracks(only_audio=True)
            }
        }

    def get_tracks(self, **kwargs):
        track_type = next(iter(kwargs))
        tracks = []

        quality_attr = "resolution" \
            if track_type in ["progressive", "only_video"] \
            else "abr"
        streams = reversed(self._yt.streams.filter(**kwargs).order_by(quality_attr))

        for stream in streams:
            stream_obj = {
                "itag": stream.itag,
                "type": track_type,
                "quality": getattr(stream, quality_attr),
                "format": stream.subtype,
                "size": self.convert_download_size(stream.filesize)
            }

            tracks.append(stream_obj)

        return tracks

    def convert_download_size(self, size_bytes):
        if size_bytes == 0:
            return "0B"

        size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
        i = int(math.floor(math.log(size_bytes, 1024)))
        p = math.pow(1024, i)
        s = round(size_bytes / p, 2)
        return f"{s}{size_name[i]}"

    def convert_length(self, length_seconds):
        m, s = divmod(length_seconds, 60)
        h, m = divmod(m, 60)

        if h > 0:
            # If there are hours, format as hh:mm:ss
            return f"{h:02d}:{m:02d}:{s:02d}"
        elif m > 0:
            # If there are minutes but no hours, format as mm:ss
            return f"{m:02d}:{s:02d}"
        else:
            # If there are only seconds, format as 0:ss
            return f"0:{s:02d}"

    def get_stream(self, itag):
        return self._yt.streams.get_by_itag(itag)


if __name__ == '__main__':
    v = Video("https://www.youtube.com/watch?v=cLArh72FEYQ")
