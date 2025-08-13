from pathlib import Path
import sys
import builtins
import subprocess
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import main
from main import load_config, build_command, sanitize_filename, is_valid_url


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


def test_is_valid_url():
    assert is_valid_url("https://example.com")
    assert not is_valid_url("example.com")
    assert not is_valid_url("http://")


def test_main_uses_default_codec(monkeypatch):
    cfg = {"defaults": {"media_type": "audio", "audio_codec": "mp3"}}
    monkeypatch.setattr(main, "load_config", lambda: cfg)
    inputs = iter(["", "http://example.com"])
    monkeypatch.setattr(builtins, "input", lambda _: next(inputs))
    recorded = {}

    def fake_run(cmd, check):
        recorded["cmd"] = cmd

    monkeypatch.setattr(subprocess, "run", fake_run)
    main.main()
    assert recorded["cmd"][recorded["cmd"].index("--audio-format") + 1] == "mp3"


def test_main_invalid_codec(monkeypatch):
    cfg = {"defaults": {"media_type": "audio", "audio_codec": "mp3"}}
    monkeypatch.setattr(main, "load_config", lambda: cfg)
    monkeypatch.setattr(builtins, "input", lambda _: "wav")
    monkeypatch.setattr(
        subprocess, "run", lambda *args, **kwargs: pytest.fail("should not run")
    )
    with pytest.raises(SystemExit) as exc:
        main.main()
    assert exc.value.code == 1


def test_main_reprompts_invalid_url(monkeypatch, capsys):
    cfg = {"defaults": {"media_type": "audio", "audio_codec": "mp3"}}
    monkeypatch.setattr(main, "load_config", lambda: cfg)
    inputs = iter(["", "not a url", "https://example.com"])
    monkeypatch.setattr(builtins, "input", lambda _: next(inputs))
    recorded = {}

    def fake_run(cmd, check):
        recorded["cmd"] = cmd

    monkeypatch.setattr(subprocess, "run", fake_run)
    main.main()
    assert recorded["cmd"][-1] == "https://example.com"
    captured = capsys.readouterr()
    assert "Invalid URL" in captured.out
