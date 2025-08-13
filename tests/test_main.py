from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from main import load_config, build_command, sanitize_filename


def test_load_config(tmp_path):
    cfg_content = """
[paths]
video = "videos"

[defaults]
media_type = "video"
"""
    cfg_file = tmp_path / "config.toml"
    cfg_file.write_text(cfg_content)
    cfg = load_config(str(cfg_file))
    assert cfg["paths"]["video"] == "videos"
    assert cfg["defaults"]["media_type"] == "video"


def test_load_config_missing(tmp_path):
    cfg = load_config(str(tmp_path / "missing.toml"))
    assert cfg == {}


def test_build_command_video():
    cfg = {
        "paths": {"video": "vids"},
        "defaults": {"output_template": "%(title)s:?*.%(ext)s"},
    }
    url = "http://example.com/video"
    cmd = build_command("video", "mp4", url, cfg)
    assert cmd == [
        "yt-dlp",
        "--restrict-filenames",
        "-P",
        Path("vids").as_posix(),
        "-o",
        "%(title)s___.%(ext)s",
        "-f",
        "bestvideo[ext=mp4]+bestaudio/best",
        url,
    ]


def test_build_command_audio():
    cfg = {"paths": {"audio": "aud"}}
    url = "http://example.com/audio"
    cmd = build_command("audio", "mp3", url, cfg)
    assert cmd == [
        "yt-dlp",
        "--restrict-filenames",
        "-P",
        Path("aud").as_posix(),
        "-x",
        "--audio-format",
        "mp3",
        url,
    ]


def test_sanitize_filename():
    name = "bad:name?file*.mp3"
    assert sanitize_filename(name) == "bad_name_file_.mp3"
