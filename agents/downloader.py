from yt_dlp import YoutubeDL
import subprocess
import os

DATA_DIR = "data"

TEMP_FILE = f"{DATA_DIR}/temp_audio.%(ext)s"
WEBM_FILE = f"{DATA_DIR}/audio.webm"
WAV_FILE = f"{DATA_DIR}/clean_audio.wav"

os.makedirs(DATA_DIR, exist_ok=True)


def download_audio(url):

    print("=" * 60)
    print("📥 Downloading highest quality audio...")
    print("=" * 60)

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": TEMP_FILE,
        "quiet": False,
        "noplaylist": True,
    }

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        downloaded_file = ydl.prepare_filename(info)

    print("✅ Download Complete")

    print("\n🎧 Converting to clean WAV...")

    subprocess.run([
        "ffmpeg",
        "-y",

        "-ss", "45",

        "-i", downloaded_file,

        "-ac", "1",

        "-ar", "16000",

        "-af", "loudnorm",

        WAV_FILE
    ], check=True)

    subprocess.run([
        "ffmpeg",
        "-y",

        "-ss", "45",

        "-i", downloaded_file,

        "-c", "copy",

        WEBM_FILE
    ], check=True)

    if os.path.exists(downloaded_file):
        os.remove(downloaded_file)

    print("✅ Audio Ready")
    print(f"WAV  : {WAV_FILE}")
    print(f"WEBM : {WEBM_FILE}")


if __name__ == "__main__":

    url = input("YouTube URL: ")

    download_audio(url)