#!/usr/bin/env python3
"""Simple command-line interface for downloading media with yt-dlp."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

try:  # Python 3.11+
    import tomllib
except ModuleNotFoundError:  # pragma: no cover
    import tomli as tomllib  # type: ignore


def load_config(path: str = "config.toml") -> dict:
    """Return configuration values loaded from *path*.

    Missing files result in an empty configuration.
    """

    try:
        with open(path, "rb") as f:
            return tomllib.load(f)
    except FileNotFoundError:
        return {}


def main() -> None:
    """Run the interactive downloader."""
    print("========== YT-DLP Helper ==========")
    print("Download audio or video from supported sites using yt-dlp.\n")

    cfg = load_config()

    media_type = cfg.get("defaults", {}).get("media_type", "").lower()
    if media_type not in {"video", "audio"}:
        media_type = input("Select media type (video/audio): ").strip().lower()
    if media_type not in {"video", "audio"}:
        print("Invalid media type. Please choose 'video' or 'audio'.")
        sys.exit(1)

    if media_type == "video":
        codecs = {"mp4": "mp4", "webm": "webm"}
        print("Available video codecs:")
        default_codec = cfg.get("defaults", {}).get("video_codec", "").lower()
        download_path = cfg.get("paths", {}).get("video")
    else:
        codecs = {"mp3": "mp3", "m4a": "m4a", "flac": "flac"}
        print("Available audio codecs:")
        default_codec = cfg.get("defaults", {}).get("audio_codec", "").lower()
        download_path = cfg.get("paths", {}).get("audio")

    for name in codecs:
        print(f"- {name}")

    codec = default_codec
    if codec not in codecs:
        codec = input("Choose codec: ").strip().lower()
    if codec not in codecs:
        print("Invalid codec selected.")
        sys.exit(1)

    url = input("Enter video URL: ").strip()
    if not url:
        print("No URL provided.")
        sys.exit(1)

    cmd = ["yt-dlp"]
    if download_path:
        cmd.extend(["-P", Path(download_path).expanduser().as_posix()])

    output_template = cfg.get("defaults", {}).get("output_template")
    if output_template:
        cmd.extend(["-o", output_template])

    try:
        if media_type == "video":
            fmt = f"bestvideo[ext={codecs[codec]}]+bestaudio/best"
            cmd.extend(["-f", fmt, url])
        else:
            cmd.extend(["-x", "--audio-format", codecs[codec], url])

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
