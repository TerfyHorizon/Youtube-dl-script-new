#!/usr/bin/env python3
"""Simple command-line interface for downloading media with yt-dlp."""

import subprocess
import sys


def main() -> None:
    """Run the interactive downloader."""
    print("========== YT-DLP Helper ==========")
    print("Download audio or video from supported sites using yt-dlp.\n")

    media_type = input("Select media type (video/audio): ").strip().lower()
    if media_type not in {"video", "audio"}:
        print("Invalid media type. Please choose 'video' or 'audio'.")
        sys.exit(1)

    if media_type == "video":
        codecs = {"mp4": "mp4", "webm": "webm"}
        print("Available video codecs:")
    else:
        codecs = {"mp3": "mp3", "m4a": "m4a", "flac": "flac"}
        print("Available audio codecs:")

    for name in codecs:
        print(f"- {name}")

    codec = input("Choose codec: ").strip().lower()
    if codec not in codecs:
        print("Invalid codec selected.")
        sys.exit(1)

    url = input("Enter video URL: ").strip()
    if not url:
        print("No URL provided.")
        sys.exit(1)

    try:
        if media_type == "video":
            fmt = f"bestvideo[ext={codecs[codec]}]+bestaudio/best"
            cmd = ["yt-dlp", "-f", fmt, url]
        else:
            cmd = ["yt-dlp", "-x", "--audio-format", codecs[codec], url]

        print("Running:", " ".join(cmd))
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as exc:
        print("Download failed:", exc)
        sys.exit(exc.returncode)
    except FileNotFoundError:
        print("yt-dlp is not installed or not found in PATH.")
        sys.exit(1)


if __name__ == "__main__":
    main()
