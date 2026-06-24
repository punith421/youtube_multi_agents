from agents.downloader import download_audio
from agents.transcriber import transcribe_audio

url = input("Enter YouTube URL: ")

download_audio(url)

transcribe_audio("data/audio.webm")