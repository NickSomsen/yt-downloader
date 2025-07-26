from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from contextlib import asynccontextmanager
from pydantic import BaseModel
from video import Video
from pytubefix.exceptions import PytubeFixError, VideoUnavailable
import os
import shutil

DOWNLOAD_DIR = "./downloads"


@asynccontextmanager
async def lifespan(app: FastAPI):
    # when application starts, ensure download_dir exists
    if not os.path.isdir(DOWNLOAD_DIR):
        os.mkdir(DOWNLOAD_DIR)

    yield

    # when application shuts down, delete all saved downloads
    shutil.rmtree(DOWNLOAD_DIR, ignore_errors=True)


app = FastAPI(lifespan=lifespan)

videos = {}


# use a data model so that FastAPI handles the parsing from the request body
class URL(BaseModel):
    url: str


# define the origins that are allowed to request this back-end
origins = [
    "http://localhost:5173",  # front-end development server origin
    "http://127.0.0.1:5173",
    "http://localhost:8080",  # docker-container http server origin
    "http://127.0.0.1:8080"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.post("/video")
async def video(url: URL):
    try:
        v = Video(url.url)
        videos[v.id] = v
        return v.json
    except VideoUnavailable as e:
        # all VideoUnavailable error messages are formatted like "<video_id> is <reason>"
        reason = str(e).split(" ", 1)[1]
        msg = f"The requested video {reason}."
        raise HTTPException(status_code=404,
                            detail=msg)
    except PytubeFixError as e:
        raise HTTPException(status_code=404,
                            detail=str(e))


@app.get("/download/{video_id}/{itag}")
async def download(video_id: str, itag: int):
    if video_id not in videos:
        raise HTTPException(status_code=404,
                            detail=f"Video with id '{video_id}' not found. Please load the video again.")

    v = videos[video_id]
    stream = v.get_stream(itag)

    if not stream:
        raise HTTPException(status_code=404,
                            detail=f"Stream with itag '{itag}' for video '{video_id}' does not exist.")

    try:
        download_filename = stream.default_filename
        save_as_name = f"{v.id}.{itag}.{download_filename.rsplit('.')[1]}"

        saved_path = stream.download(output_path=DOWNLOAD_DIR,
                                     filename=save_as_name)

        return FileResponse(saved_path,
                            filename=download_filename,
                            headers={"Access-Control-Expose-Headers": "Content-Disposition"})
    except Exception as e:
        print(repr(e))
        raise HTTPException(status_code=500,
                            detail="An unexpected error occurred. Please try again later.")
