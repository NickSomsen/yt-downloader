## YTDownloader

Easily download YouTube videos using just the video URL🔗.

![screenshot](yt-downloader_ss.png)

Created by Nick Somsen using [pytube](https://github.com/pytube/pytube).

### Project

- Front-end: Vue + Vuetify app with Vite as build tool.
- Back-end: Python back-end with FastAPI

### Usage
1. Install dependencies: use `package.json` for front-end and `requirements.txt` for back-end.
2. Run front-end on `http://localhost:5173` (or add other origin to back-end `main.py`).
3. Run back-end FastAPI server.
4. Open front-end URL in browser and start downloading!

### Known issues
Images are not part of front-end build because of issues with `@` alias for `img` src.
