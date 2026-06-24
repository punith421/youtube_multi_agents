from yt_dlp import YoutubeDL

def download_audio(url):
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": "data/audio.%(ext)s",
    }

    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    print("Audio downloaded successfully!")