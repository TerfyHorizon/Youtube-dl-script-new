# YT-DLP Helper

Simple interactive wrapper around [yt-dlp](https://github.com/yt-dlp/yt-dlp) for quick audio or video downloads.

## Installation

Install dependencies:

```bash
pip install -r requirements.txt
```

## Configuration

Runtime options can be preconfigured via a `config.toml` file in the project directory.

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

Any missing value will trigger an interactive prompt when running `main.py`.

## Usage

Run the downloader:

```bash
python main.py
```
