# Mux-Sub

> Automatically mux subtitles, fonts, chapters, and metadata into your videos using FFmpeg.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![FFmpeg](https://img.shields.io/badge/FFmpeg-required-green.svg)](https://ffmpeg.org/)

Mux-Sub is a universal FFmpeg-powered muxer designed for anime, donghua, TV series, and fansub releases. It automatically matches episodes with subtitles, embeds fonts, adds optional chapter markers, preserves audio tracks and metadata, and generates clean output filenames using customizable templates.

---

## Features

- **Automatic episode-to-subtitle matching** from common naming schemes
- **Fallback positional matching** — if no episode numbers are detected, files are paired alphabetically 1-to-1
- **Already-muxed detection** — skips files that were previously processed by Mux-Sub
- **Multiple subtitle formats** — ASS, SSA, SRT, VTT, SUB (with ASS prioritized; all converted to ASS in output)
- **Font embedding** — all fonts in `sub/font/` are automatically attached
- **Chapter/jump point support** — optional chapter markers for media players
- **Lossless output** — video and audio are copied without re-encoding
- **Metadata & language preservation** — all track info carried over
- **Custom output naming** — flexible template system for filenames
- **Always outputs MKV** — regardless of source container format

---

## Requirements

- Python 3.8+
- [FFmpeg](https://ffmpeg.org/download.html)
- FFprobe (included with FFmpeg)

Verify your installation:

```bash
ffmpeg -version
ffprobe -version
```

---

## Installation

**Clone the repository:**

```bash
git clone https://github.com/Shridhuu/Mux-Sub.git
cd Mux-Sub
```

Or simply download `main.py` and place it in your release folder.

---

## Folder Structure

1. Create a folder and put all your **episode files** inside it. Make sure both the episodes and subtitles have episode numbers in their filenames so Mux-Sub can match them correctly.
2. Inside that folder, create a subfolder called **`sub/`** and place all your subtitle files there.
3. Inside `sub/`, create another subfolder called **`font/`** and place all your font files there.
4. Place **`main.py`** in the root folder alongside the episodes — not inside `sub/` or `font/`.

```
Series Folder/
├── main.py          ← script goes here
├── 1.mkv
├── 2.mkv
├── 3.mkv
│
└── sub/
    ├── 1.ass
    ├── 2.ass
    ├── 3.ass
    │
    └── font/
        ├── font1.ttf
        ├── font2.otf
        └── font3.ttc
```

---

## Usage

Open a terminal in the same folder as your episodes and run:

```bash
python3 main.py
```

### Series Name

Series name is optional. Leave it blank and the original filename will be used instead.

```
Series Name (optional): Stellar Transformation
```

### Output Template

You can leave this blank or define a custom naming format using [template variables](#template-variables).

**Custom template:**
```
{series} S7-{ep2} [4K 8Bits E-AC-3 & AAC-LC]
```

**Output:**
```
Stellar Transformation S7-01 [4K 8Bits E-AC-3 & AAC-LC].mkv
Stellar Transformation S7-02 [4K 8Bits E-AC-3 & AAC-LC].mkv
```

**Default (blank template):**
```
Stellar Transformation EP01.mkv
Stellar Transformation EP02.mkv
```

---

## Template Variables

| Variable | Description |
|---|---|
| `{series}` | Series name |
| `{ep}` | Episode number |
| `{ep2}` | Episode number with leading zero |
| `{video_stem}` | Original filename without extension |

**Examples:**

```
{series} EP{ep2}
{series} S7-{ep2} [4K 8Bits E-AC-3 & AAC-LC]
{series} - {ep2}
{video_stem}
```

---

## Supported Video Formats

| Format | Extension |
|---|---|
| Matroska | `.mkv` |
| MPEG-4 | `.mp4` |
| iTunes Video | `.m4v` |
| QuickTime | `.mov` |
| AVI | `.avi` |
| WebM | `.webm` |

> Regardless of input format, the output is always an `.mkv` file.

---

## Supported Episode Formats

Mux-Sub automatically detects episode numbers from a wide range of filename patterns:

| Pattern | Example |
|---|---|
| `S##E##` | `Stellar Transformation S07E01.mkv` |
| `#x##` | `7x01.mkv` |
| `EP##` | `EP01.mkv` |
| `Episode ##` | `Episode 01.mkv` |
| `##` | `01.mkv` |
| `###` | `001.mkv` |

---

## Subtitle Priority

When multiple subtitle formats exist for the same episode, Mux-Sub selects the best one automatically:

1. ASS
2. SSA
3. SRT
4. VTT
5. SUB

Styled subtitles (ASS/SSA) are always preferred when available.

---

## Jump Points (Chapters)

Chapter markers are optional and will appear in supported media players.

When prompted:

```
Add jump points? (y/n): y
```

Enter your chapters in `Label|MM:SS` or `Label|HH:MM:SS` format:

```
Opening|00:00
Episode Title & Number|02:32
Episode|02:35
```

---

## Font Attachments

All font files inside `sub/font/` are automatically embedded into the output MKV.

**Supported formats:** `.ttf`, `.otf`, `.ttc`

---

## What Gets Preserved / Removed

| Preserved | Removed |
|---|---|
| Video streams | Existing cover art streams |
| Audio streams | Original subtitle tracks |
| Metadata | |
| Language information | |
| Attached fonts | |

---

## Notes

- Video and audio streams are copied directly — **no quality loss**.
- All subtitle formats are **converted to ASS** in the output and tagged as English (`language=eng`).
- Files already processed by Mux-Sub are **automatically skipped** on subsequent runs.
- If no episode numbers are found in filenames, files are **paired alphabetically** in order.
- Source files are removed only after **successful** muxing.
- FFmpeg and FFprobe must be accessible from your system `PATH`.
- Existing cover art is intentionally ignored during muxing.

---

## Disclaimer

Mux-Sub is a **muxing utility only**. It does not encode video, encode audio, modify quality, or alter the original media streams in any way. All video and audio are copied directly using FFmpeg.

---

## License

This project is licensed under the [MIT License](LICENSE).

---

## Author

Created by **Shridhuu**

GitHub: [https://github.com/Shridhuu](https://github.com/Shridhuu)
