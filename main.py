from pathlib import Path
import subprocess
import re
import sys

VIDEO_DIR = Path(".")
SUB_DIR = VIDEO_DIR / "sub"
FONT_DIR = SUB_DIR / "font"

SUB_EXTENSIONS = {".ass", ".ssa", ".srt", ".vtt", ".sub"}
SUB_PREFERENCE = {".ass": 0, ".ssa": 1, ".srt": 2, ".vtt": 3, ".sub": 4}
VIDEO_EXTENSIONS = {".mkv", ".mp4", ".m4v", ".mov", ".avi", ".webm"}
MUX_TAG = "universal_mux_v1"

def extract_episode(name):
    patterns = [
        r"(?i)s\d+e(\d+)",
        r"(?i)(\d+)x(\d+)",
        r"(?i)(?:ep|episode)[\s._-]*(\d+)",
        r"(?i)(?:^|[\s._-])(\d{1,3})(?:$|[\s._-])",
    ]
    for pattern in patterns:
        m = re.search(pattern, name)
        if m:
            if len(m.groups()) >= 2 and m.group(2):
                return int(m.group(2))
            if m.group(1):
                return int(m.group(1))
    nums = re.findall(r"(?<!\d)(\d{1,3})(?!\d)", name)
    if nums:
        return int(nums[-1])
    return None

def parse_time_to_ms(text):
    parts = text.strip().split(":")
    if len(parts) == 2:
        h = 0
        m, s = parts
    elif len(parts) == 3:
        h, m, s = parts
    else:
        raise ValueError("Bad time format")
    if "." in s:
        sec, frac = s.split(".", 1)
        frac = (frac + "000")[:3]
    else:
        sec = s
        frac = "000"
    return ((int(h) * 3600) + (int(m) * 60) + int(sec)) * 1000 + int(frac)

def is_already_muxed(path):
    cmd = [
        "ffprobe",
        "-v", "error",
        "-show_entries", "format_tags=muxed_by",
        "-of", "default=nk=1:nw=1",
        str(path),
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=False)
        return result.stdout.strip() == MUX_TAG
    except Exception:
        return False

series_name = input("Series Name (optional): ").strip()
output_template = input("Output Template (optional, blank = Series EPxx): ").strip()
add_jump_points = input("Add jump points? (y/n): ").strip().lower().startswith("y")

chapter_file = None

if add_jump_points:
    print("Enter jump points as Name|MM:SS or Name|HH:MM:SS")
    print("Leave blank to finish")
    entries = []
    while True:
        line = input("> ").strip()
        if not line:
            break
        if "|" not in line:
            print("Use Name|MM:SS")
            continue
        title, time_text = line.split("|", 1)
        title = title.strip()
        time_text = time_text.strip()
        try:
            start_ms = parse_time_to_ms(time_text)
            entries.append((title, start_ms))
        except ValueError:
            print("Bad time format")
    if entries:
        chapter_file = VIDEO_DIR / ".jump_points.ffmeta"
        text = ";FFMETADATA1\n"
        for i, (title, start_ms) in enumerate(entries):
            end_ms = entries[i + 1][1] if i + 1 < len(entries) else 999999999
            text += (
                "\n[CHAPTER]\n"
                "TIMEBASE=1/1000\n"
                f"START={start_ms}\n"
                f"END={end_ms}\n"
                f"title={title}\n"
            )
        chapter_file.write_text(text, encoding="utf-8")

fonts = []
if FONT_DIR.exists():
    fonts = sorted(
        [f for f in FONT_DIR.iterdir() if f.is_file() and f.suffix.lower() in {".ttf", ".otf", ".ttc"}],
        key=lambda p: p.name.lower()
    )

video_files = sorted(
    [
        p for p in VIDEO_DIR.iterdir()
        if p.is_file()
        and p.suffix.lower() in VIDEO_EXTENSIONS
        and p.name != "test.mkv"
        and not p.name.startswith("temp_")
        and not p.name.startswith(".mux_")
    ],
    key=lambda p: p.name.lower()
)

subtitle_files = sorted(
    [p for p in SUB_DIR.rglob("*") if p.is_file() and p.suffix.lower() in SUB_EXTENSIONS],
    key=lambda p: (SUB_PREFERENCE.get(p.suffix.lower(), 99), p.name.lower())
)

if not video_files:
    print("No video files found.")
    if chapter_file and chapter_file.exists():
        chapter_file.unlink()
    sys.exit(0)

video_by_ep = {}
video_order = []
for video in video_files:
    if is_already_muxed(video):
        continue
    ep = extract_episode(video.stem)
    video_order.append((video, ep))
    if ep is not None and ep not in video_by_ep:
        video_by_ep[ep] = video

subtitle_by_ep = {}
subtitle_order = []
for sub in subtitle_files:
    ep = extract_episode(sub.stem)
    subtitle_order.append((sub, ep))
    if ep is not None:
        current = subtitle_by_ep.get(ep)
        if current is None:
            subtitle_by_ep[ep] = sub
        else:
            current_rank = (SUB_PREFERENCE.get(current.suffix.lower(), 99), current.name.lower())
            new_rank = (SUB_PREFERENCE.get(sub.suffix.lower(), 99), sub.name.lower())
            if new_rank < current_rank:
                subtitle_by_ep[ep] = sub

paired = []
used_videos = set()
used_subs = set()

for ep in sorted(set(video_by_ep) & set(subtitle_by_ep)):
    v = video_by_ep[ep]
    s = subtitle_by_ep[ep]
    paired.append((v, s, ep))
    used_videos.add(v)
    used_subs.add(s)

remaining_videos = [v for v, ep in video_order if v not in used_videos]
remaining_subs = [s for s, ep in subtitle_order if s not in used_subs]

if not paired and len(remaining_videos) == len(remaining_subs) and remaining_videos:
    remaining_videos = sorted(remaining_videos, key=lambda p: p.name.lower())
    remaining_subs = sorted(
        remaining_subs,
        key=lambda p: (SUB_PREFERENCE.get(p.suffix.lower(), 99), p.name.lower())
    )
    for i, video in enumerate(remaining_videos):
        subtitle = remaining_subs[i]
        ep = i + 1
        paired.append((video, subtitle, ep))

paired = sorted(paired, key=lambda x: (x[2], x[0].name.lower()))

if not paired:
    print("No matching episodes found.")
    if chapter_file and chapter_file.exists():
        chapter_file.unlink()
    sys.exit(0)

print(f"Found {len(fonts)} font(s)")
for font in fonts:
    print(font.name)

print(f"Matched {len(paired)} item(s)")

for video, subtitle, ep in paired:
    if output_template:
        out_name = output_template.format(
            series=series_name,
            ep=ep,
            ep2=f"{ep:02d}",
            video_stem=video.stem
        ).strip()
    elif series_name:
        out_name = f"{series_name} EP{ep:02d}"
    else:
        out_name = video.stem

    if not out_name.lower().endswith(".mkv"):
        out_name += ".mkv"

    final_output = VIDEO_DIR / out_name
    temp_output = VIDEO_DIR / f".mux_{video.stem}.mkv"

    cmd = [
        "ffmpeg",
        "-hide_banner",
        "-loglevel", "warning",
        "-y",
        "-i", str(video),
        "-i", str(subtitle),
    ]

    if chapter_file is not None:
        cmd += ["-i", str(chapter_file)]

    cmd += [
        "-map", "0:v:0",
        "-map", "0:a?",
        "-map", "1:0",
        "-map_metadata", "0",
    ]

    if chapter_file is not None:
        cmd += ["-map_chapters", "2"]

    cmd += [
        "-c:v", "copy",
        "-c:a", "copy",
        "-c:s", "ass",
        "-disposition:s:0", "default",
        "-metadata:s:s:0", "language=eng",
        "-metadata:s:s:0", "title=English",
        "-metadata", f"muxed_by={MUX_TAG}",
    ]

    for idx, font in enumerate(fonts):
        mime = "application/vnd.ms-opentype" if font.suffix.lower() == ".otf" else "application/x-truetype-font"
        cmd += [
            "-attach", str(font),
            f"-metadata:s:t:{idx}", f"mimetype={mime}",
            f"-metadata:s:t:{idx}", f"filename={font.name}",
        ]

    cmd.append(str(temp_output))

    print(f"[EP{ep:02d}] {video.name} + {subtitle.name}")

    try:
        subprocess.run(cmd, check=True)

        if final_output.exists() and final_output.resolve() != video.resolve():
            final_output.unlink()

        if temp_output.exists():
            if video.resolve() == final_output.resolve():
                video.unlink()
                temp_output.replace(final_output)
            else:
                video.unlink()
                temp_output.replace(final_output)

        print(f"[EP{ep:02d}] Done")
    except subprocess.CalledProcessError:
        print(f"[EP{ep:02d}] Failed")
        if temp_output.exists():
            temp_output.unlink()

if chapter_file and chapter_file.exists():
    chapter_file.unlink()

print("Done.")
