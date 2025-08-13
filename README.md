# YT-DLP Helper

## Overview

YT-DLP Helper is a small interactive wrapper around [yt-dlp](https://github.com/yt-dlp/yt-dlp) that guides you through downloading audio or video from supported sites. It asks a few questions and then runs yt-dlp with sane defaults, making quick media grabs less error‑prone.

## Setup

### 1. Install dependencies

This project requires Python 3.9+ with yt-dlp available on your system:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

The download/convert functionality also relies on `ffmpeg` being installed and discoverable in your `PATH`.

### 2. Configure defaults

Copy the example configuration and edit it to suit your preferences:

```bash
cp config.example.toml config.toml
```

`config.toml` lets you set default download folders, preferred codecs and an optional output template.

```toml
[paths]
# Where to store downloaded media
video = "downloads/videos"
audio = "downloads/audio"

[defaults]
# Choose default media type and codecs
media_type = "video"
video_codec = "mp4"
audio_codec = "mp3"
# Optional custom output template
output_template = "%(title)s.%(ext)s"
```

Any values you omit will be requested interactively each run. Downloaded filenames are sanitized to remove characters invalid on common filesystems.

## Usage

Launch the helper and respond to the prompts:

```bash
python main.py
```

### Example: video download

```
$ python main.py
========== YT-DLP Helper ==========
Download audio or video from supported sites using yt-dlp.

Select media type (video/audio): video
Available video codecs:
- mp4
- webm
Choose codec: mp4
Enter video URL: https://www.youtube.com/watch?v=dQw4w9WgXcQ
Running: yt-dlp --restrict-filenames -P downloads/videos -f bestvideo[ext=mp4]+bestaudio/best https://www.youtube.com/watch?v=dQw4w9WgXcQ
```

### Example: audio download

```
$ python main.py
========== YT-DLP Helper ==========
Download audio or video from supported sites using yt-dlp.

Select media type (video/audio): audio
Available audio codecs:
- mp3
- m4a
- flac
Choose codec: mp3
Enter video URL: https://www.youtube.com/watch?v=dQw4w9WgXcQ
Running: yt-dlp --restrict-filenames -x --audio-format mp3 https://www.youtube.com/watch?v=dQw4w9WgXcQ
```

## Troubleshooting

- **`yt-dlp is not installed`** – Ensure `pip install -r requirements.txt` completed successfully and that the virtual environment is activated.
- **`ffmpeg not found`** – yt-dlp needs ffmpeg for format conversions. Install it with your system package manager.
- **Invalid codec or media type** – The helper accepts only the codecs listed in the prompts (`mp4`, `webm`, `mp3`, `m4a`, `flac`).

## Contributing

Contributions are welcome! To propose a change:

1. Fork the repository and create a topic branch.
2. Make your changes and add tests if appropriate.
3. Run the test suite with `pytest` to ensure everything passes.
4. Open a pull request describing your changes.

## Testing

Run the unit tests with [pytest](https://docs.pytest.org/):

```bash
pytest
```
