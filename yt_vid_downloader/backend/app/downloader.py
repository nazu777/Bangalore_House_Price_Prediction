from yt_dlp import YoutubeDL
import os


DOWNLOAD_DIR = "app/downloads"


def get_best_height(formats, preferred):

    preferred = int(preferred.replace("p", ""))

    heights = []

    for f in formats:

        if (
            f.get("height")
            and f.get("vcodec") != "none"
        ):
            heights.append(f["height"])

    heights = sorted(set(heights))

    if preferred in heights:
        return preferred

    higher = [x for x in heights if x > preferred]

    if higher:
        return min(higher)

    lower = [x for x in heights if x < preferred]

    if lower:
        return max(lower)

    return heights[-1]


def analyze_url(url):

    ydl_opts = {
        "quiet": True,
        "skip_download": True,
        "noplaylist": False,

        # anti-block
        "cookiesfrombrowser": ("chrome",),
        "retries": 10,
        "fragment_retries": 10,
        "sleep_interval": 2,
        "http_chunk_size": 10485760,
    }

    with YoutubeDL(ydl_opts) as ydl:

        info = ydl.extract_info(
            url,
            download=False
        )

        if "entries" in info:

            entries = list(info["entries"])

            qualities = set()

            videos = []

            for entry in entries:

                if not entry:
                    continue

                q = set()

                for f in entry.get("formats", []):

                    if (
                        f.get("height")
                        and f.get("vcodec") != "none"
                    ):

                        quality = f"{f['height']}p"

                        q.add(quality)
                        qualities.add(quality)

                videos.append({
                    "title": entry.get("title"),
                    "url": entry.get("webpage_url"),
                    "thumbnail": entry.get("thumbnail"),
                    "qualities": sorted(
                        list(q),
                        key=lambda x: int(x[:-1]),
                        reverse=True
                    )
                })

            return {
                "type": "playlist",
                "title": info.get("title"),
                "videos": videos,
                "qualities": sorted(
                    list(qualities),
                    key=lambda x: int(x[:-1]),
                    reverse=True
                )
            }

        qualities = set()

        for f in info.get("formats", []):

            if (
                f.get("height")
                and f.get("vcodec") != "none"
            ):

                qualities.add(f"{f['height']}p")

        return {
            "type": "single",
            "title": info.get("title"),
            "thumbnail": info.get("thumbnail"),
            "qualities": sorted(
                list(qualities),
                key=lambda x: int(x[:-1]),
                reverse=True
            )
        }


def download_video(url, quality):

    ydl_opts = {
        "quiet": False,

        "merge_output_format": "mp4",

        "outtmpl": os.path.join(
            DOWNLOAD_DIR,
            "%(title)s.%(ext)s"
        ),

        "noplaylist": True,

        # anti-block
        "cookiesfrombrowser": ("chrome",),
        "retries": 10,
        "fragment_retries": 10,
        "sleep_interval": 2,
        "http_chunk_size": 10485760,
    }

    with YoutubeDL(ydl_opts) as ydl:

        info = ydl.extract_info(
            url,
            download=False
        )

        height = get_best_height(
            info["formats"],
            quality
        )

        ydl_opts["format"] = (
            f"bestvideo[height={height}]"
            f"+bestaudio/"
            f"best[height={height}]"
        )

    with YoutubeDL(ydl_opts) as ydl:

        info = ydl.extract_info(
            url,
            download=True
        )

        filename = ydl.prepare_filename(info)

        base, _ = os.path.splitext(filename)

        mp4_file = base + ".mp4"

        if os.path.exists(mp4_file):
            return mp4_file

        return filename