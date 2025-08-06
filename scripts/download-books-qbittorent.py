#!/usr/bin/env -S uv --quiet run --script

# /// script
# dependencies = [
#   "qbittorrent-api",
# ]
# ///

import os
import sys
import shutil
import qbittorrentapi
import requests


QBITTORRENT_HOST = os.environ["QBITTORRENT_HOST"]
QBITTORRENT_USERNAME = os.environ["QBITTORRENT_USERNAME"]
QBITTORRENT_PASSWORD = os.environ["QBITTORRENT_PASSWORD"]


# TODO: it would be better to use SFTP as it does not consume bandwidth
HTTP_HOST = os.environ["HTTP_HOST"]
HTTP_USERNAME = os.environ["HTTP_USERNAME"]
HTTP_PASSWORD = os.environ["HTTP_PASSWORD"]
HTTP_BASE_PATH = "downloads/qbittorrent"


FROM_CATEGORY = "books"
TO_CATEGORY = "books-downloaded"

PROGRESS_BAR_LENGTH = 50


def get_string_after_first_slash(s):
    # Find the index of the first '/'
    index = s.find("/")
    # Return the substring after the first '/'
    if index != -1:
        return s[index + 1 :]
    return s


if __name__ == "__main__":
    if not QBITTORRENT_HOST or not QBITTORRENT_USERNAME or not QBITTORRENT_PASSWORD:
        print(
            "Please set QBITTORRENT_HOST, QBITTORRENT_USERNAME, and QBITTORRENT_PASSWORD environment variables."
        )
        exit(1)

    if not HTTP_HOST or not HTTP_USERNAME or not HTTP_PASSWORD:
        print(
            "Please set HTTP_HOST, HTTP_USERNAME, and HTTP_PASSWORD environment variables."
        )
        exit(1)

    qbt_client = qbittorrentapi.Client(
        host=QBITTORRENT_HOST,
        username=QBITTORRENT_USERNAME,
        password=QBITTORRENT_PASSWORD,
    )

    try:
        qbt_client.auth_log_in()
    except qbittorrentapi.LoginFailed as e:
        print(e)
        sys.exit(1)

    workdir = "book_downloads"
    os.makedirs(workdir, exist_ok=True)

    for torrent in qbt_client.torrents_info(
        category="books", status_filter="completed"
    ):
        print(f"Downloading {torrent.name}...")
        local_dir = os.path.join(workdir, torrent.name)
        os.makedirs(local_dir, exist_ok=True)

        for file in torrent.files:
            file_name = get_string_after_first_slash(file.name)
            print(f" -> {file_name}")
            path = f"{torrent.name}/{file_name}"

            local_path = os.path.join(local_dir, file_name)

            if os.path.exists(local_path) and os.path.getsize(local_path) == file.size:
                print(f"   File {local_path} already exists, skipping download.")
                continue

            res = requests.get(
                f"{HTTP_HOST}/{HTTP_BASE_PATH}/{path}",
                params={"hashes": torrent.hash, "category": FROM_CATEGORY},
                auth=(HTTP_USERNAME, HTTP_PASSWORD),
            )

            with open(local_path, "wb") as f:
                total_length = res.headers.get("content-length")

                if total_length is None:  # no content length header
                    f.write(res.content)
                else:
                    dl = 0
                    total_length = int(total_length)
                    for data in res.iter_content(chunk_size=4096):
                        dl += len(data)
                        f.write(data)
                        done = int(PROGRESS_BAR_LENGTH * dl / total_length)
                        sys.stdout.write(
                            f"\r[{'=' * done}>{' ' * (PROGRESS_BAR_LENGTH - done - 1)}] ({dl}/{total_length} bytes)"
                        )
                        sys.stdout.flush()
                print(f"\r{' ' * PROGRESS_BAR_LENGTH * 2}", end="\r")
                sys.stdout.flush()

    # Zip the downloaded files
    zip_file_path = "books.zip"
    shutil.make_archive(zip_file_path.replace(".zip", ""), "zip", workdir)

    print(f"Zipped downloaded files to {zip_file_path}")
