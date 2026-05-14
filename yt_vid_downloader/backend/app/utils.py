import os
import shutil
import zipfile


DOWNLOAD_DIR = "app/downloads"

os.makedirs(DOWNLOAD_DIR, exist_ok=True)


def clean_downloads():

    if os.path.exists(DOWNLOAD_DIR):
        shutil.rmtree(DOWNLOAD_DIR)

    os.makedirs(DOWNLOAD_DIR, exist_ok=True)


def create_zip(files):

    zip_path = os.path.join(
        DOWNLOAD_DIR,
        "videos.zip"
    )

    with zipfile.ZipFile(
        zip_path,
        "w",
        zipfile.ZIP_DEFLATED
    ) as zipf:

        for file in files:

            zipf.write(
                file,
                arcname=os.path.basename(file)
            )

    return zip_path