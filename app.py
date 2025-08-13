from flask import Flask, send_file
import yt_dlp
import os

app = Flask(__name__)

@app.route("/download/song/<video_id>")
def download_song(video_id):
    link = f"https://youtu.be/{video_id}"
    file_path = f"downloads/{video_id}.mp3"
    os.makedirs("downloads", exist_ok=True)

    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': file_path,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '320',
        }],
        'quiet': True
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([link])
        return send_file(file_path, as_attachment=True)
    except Exception as e:
        return {"error": str(e)}

@app.route("/")
def home():
    return {"message": "YouTube to MP3 API is running!"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
