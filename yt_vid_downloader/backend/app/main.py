from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.concurrency import run_in_threadpool

from .models import (
    URLRequest,
    DownloadRequest
)

from .downloader import (
    analyze_url,
    download_video
)

from .utils import (
    clean_downloads,
    create_zip
)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {"message": "Backend Running"}


@app.post("/analyze")
def analyze(req: URLRequest):

    clean_downloads()

    response = []

    for url in req.urls:

        try:

            data = analyze_url(url)

            response.append(data)

        except Exception as e:

            response.append({
                "error": str(e)
            })

    return response


@app.post("/download")
async def download(req: DownloadRequest):

    files = []

    for url in req.urls:

        data = analyze_url(url)

        if data["type"] == "single":

            file = await run_in_threadpool(
                download_video,
                url,
                req.quality
            )

            files.append(file)

        else:

            for video in data["videos"]:

                file = await run_in_threadpool(
                    download_video,
                    video["url"],
                    req.quality
                )

                files.append(file)

    if len(files) == 1:

        return FileResponse(
            files[0],
            media_type="video/mp4",
            filename=files[0].split("/")[-1]
        )

    zip_path = create_zip(files)

    return FileResponse(
        zip_path,
        media_type="application/zip",
        filename="videos.zip"
    )